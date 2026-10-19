import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from . import collectors as C
from .db import connect
from .score import Matrix

CFG = Path(__file__).resolve().parents[2] / "config"


def load():
    return (yaml.safe_load((CFG / "sources.yaml").read_text()),
            yaml.safe_load((CFG / "keywords.yaml").read_text()))


def store(con, matrix, items, collector):
    now = datetime.now(timezone.utc).isoformat()
    inserted = 0
    for it in items:
        score, matched, relevant = matrix.score(it["title"], it["summary"])
        if it["source"].startswith("GN") and score > 0:
            relevant = True  # Google News results are already topic-filtered by the search query; titles are short
        cur = con.execute(
            "INSERT OR IGNORE INTO articles(url,title,source,source_type,reliability,lang,published,fetched_at,summary,score,matched,relevant)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (it["url"], it["title"], it["source"], it["type"], it["reliability"], it["lang"],
             it["published"], now, it["summary"], score, matched, int(relevant)))
        inserted += cur.rowcount
    con.execute("INSERT INTO runs(started_at,collector,fetched,inserted) VALUES(?,?,?,?)", (now, collector, len(items), inserted))
    con.commit()
    return inserted


def cmd_collect(args):
    sources, kw = load()
    matrix = Matrix.from_config(kw)
    con = connect()
    q = kw["api_queries"]
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    jobs = [(m["name"], lambda m=m: C.rss(m)) for m in sources["rss"]]
    a = sources["apis"]
    jobs += [("nvd", lambda: C.nvd(a["nvd"], q["nvd"], since)),
             ("arxiv", lambda: C.arxiv(a["arxiv"], q["arxiv"])),
             ("gnews", lambda: C.gnews(a["gnews"], q["gnews"])),
             ("hn", lambda: C.hn(a["hn"], q["hn"], since)),
             ("ghsa", lambda: C.ghsa(a["ghsa"], q["ghsa_filter"]))]
    if args.only:
        jobs = [j for j in jobs if j[0] in args.only]
    for name, fn in jobs:
        try:
            items = fn()
            n = store(con, matrix, items, name)
            print(f"[ok]   {name:<22} fetched={len(items):<4} new={n}")
        except Exception as e:  # one broken source must not stop the run
            con.execute("INSERT INTO runs(started_at,collector,error) VALUES(?,?,?)",
                        (datetime.now(timezone.utc).isoformat(), name, str(e)[:300]))
            con.commit()
            print(f"[FAIL] {name:<22} {e}", file=sys.stderr)


def cmd_rescore(_):
    """Re-apply the keyword matrix to everything stored (after editing keywords.yaml)."""
    _, kw = load()
    matrix = Matrix.from_config(kw)
    con = connect()
    for r in con.execute("SELECT id,title,summary,source FROM articles").fetchall():
        s, m, rel = matrix.score(r["title"], r["summary"])
        if r["source"].startswith("GN") and s > 0:
            rel = True
        con.execute("UPDATE articles SET score=?, matched=?, relevant=? WHERE id=?", (s, m, int(rel), r["id"]))
    con.commit()
    print("rescored")


def cmd_stats(_):
    con = connect()
    t = con.execute("SELECT COUNT(*) n, SUM(relevant) r, MIN(published) a, MAX(published) b FROM articles").fetchone()
    print(f"articles={t['n']} relevant={t['r']} range={t['a']} -> {t['b']}")
    print("\nrelevant by source:")
    for r in con.execute("SELECT source, source_type, COUNT(*) n FROM articles WHERE relevant=1 GROUP BY source ORDER BY n DESC"):
        print(f"  {r['source']:<22} {r['source_type']:<10} {r['n']}")
    print("\nlast errors:")
    for r in con.execute("SELECT started_at, collector, error FROM runs WHERE error IS NOT NULL ORDER BY id DESC LIMIT 5"):
        print(f"  {r['started_at'][:16]} {r['collector']}: {r['error'][:80]}")


def cmd_top(args):
    con = connect()
    for r in con.execute("SELECT * FROM articles WHERE relevant=1 ORDER BY score DESC, published DESC LIMIT ?", (args.n,)):
        print(f"[{r['score']:>2}] {r['published'][:10] if r['published'] else '?':<10} {r['source']:<18} {r['title'][:90]}\n     {r['url']}")


JSONL = Path(__file__).resolve().parents[2] / "data" / "relevant.jsonl"
COLS = ["url", "title", "source", "source_type", "reliability", "lang", "published", "fetched_at",
        "summary", "score", "matched", "relevant", "status"]


def cmd_export(_):
    """Write relevant articles to a deterministic JSONL file (small, diff-friendly, safe to commit)."""
    con = connect()
    rows = con.execute(f"SELECT {','.join(COLS)} FROM articles WHERE relevant=1 ORDER BY url").fetchall()
    JSONL.parent.mkdir(parents=True, exist_ok=True)
    JSONL.write_text("".join(json.dumps(dict(r), ensure_ascii=False, sort_keys=True) + "\n" for r in rows))
    print(f"exported {len(rows)} articles -> {JSONL.name}")
    for name, query in (("sheets", "SELECT * FROM sheets ORDER BY url"), ("prompt_log", "SELECT * FROM prompt_log ORDER BY id")):
        rs = [dict(r) for r in con.execute(query)]
        if rs:
            (JSONL.parent / f"{name}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rs))
            print(f"exported {len(rs)} rows -> {name}.jsonl")


def cmd_import(_):
    """Load the JSONL back into the database (used by CI to rebuild state before collecting)."""
    if not JSONL.exists():
        print("nothing to import")
        return
    con = connect()
    n = 0
    for line in JSONL.read_text().splitlines():
        d = json.loads(line)
        cur = con.execute(f"INSERT OR IGNORE INTO articles({','.join(COLS)}) VALUES({','.join('?' * len(COLS))})",
                          [d.get(c) for c in COLS])
        n += cur.rowcount
    for name in ("sheets", "prompt_log"):
        f = JSONL.parent / f"{name}.jsonl"
        if f.exists():
            for line in f.read_text().splitlines():
                d = json.loads(line)
                d.pop("id", None)
                con.execute(f"INSERT OR IGNORE INTO {name}({','.join(d)}) VALUES({','.join('?' * len(d))})", list(d.values()))
    con.commit()
    print(f"imported {n} articles")


def cmd_sheet(args):
    """Draft source sheets for the best unreviewed articles (costs API credits; capped by --max-usd)."""
    import anthropic
    from . import sheets as S
    S.load_env()
    client, con = anthropic.Anthropic(), connect()
    if args.url:
        rows = con.execute("SELECT * FROM articles WHERE url IN (%s)" % ",".join("?" * len(args.url)), args.url).fetchall()
    else:
        rows = con.execute(
            "SELECT * FROM articles a WHERE relevant=1 AND source NOT LIKE 'GN%' AND source != 'Hacker News'"
            " AND NOT EXISTS (SELECT 1 FROM sheets s WHERE s.url=a.url)"
            " ORDER BY reliability DESC, score DESC, published DESC LIMIT 500").fetchall()
        picked, per = [], {}
        for r in rows:  # diversity: cap the number of sheets per source
            if per.get(r["source"], 0) < args.per_source:
                picked.append(r)
                per[r["source"]] = per.get(r["source"], 0) + 1
            if len(picked) >= args.top:
                break
        rows = picked
    spent = 0.0
    for a in rows:
        if spent >= args.max_usd:
            print(f"budget cap reached (${spent:.3f} >= ${args.max_usd})")
            break
        try:
            r = S.make_sheet(con, client, a)
        except Exception as e:
            print(f"[FAIL] {a['source']}: {a['title'][:60]} -> {e}", file=sys.stderr)
            continue
        spent += r.get("cost", 0)
        print(f"[{r['status']:<7}] {r.get('quotes', '-'):>5} quotes  ${r.get('cost', 0):.4f}  {a['source'][:18]:<18} {a['title'][:60]}")
    print(f"total spent this run: ${spent:.4f}")


def cmd_render(_):
    """Render all sheets to data/sheets.md for human review."""
    con = connect()
    out = ["# Source sheets (drafts to review)\n"]
    for r in con.execute("SELECT s.*, a.title, a.source, a.source_type, a.lang, a.published FROM sheets s "
                         "JOIN articles a USING(url) ORDER BY a.reliability DESC, a.published DESC"):
        d = json.loads(r["sheet"])
        out.append(f"## {r['title']}\n")
        out.append(f"- **URL**: {r['url']}\n- **Publisher**: {r['source']} ({d['publisher']}) | **Language**: {r['lang']} | "
                   f"**Date**: {(r['published'] or '?')[:10]}\n- **Source type**: {r['source_type']} | "
                   f"**Reliability prior**: {d['reliability_prior']}/5 | **Review**: {r['review']}\n"
                   f"- **Text analysed**: {r['text_kind']}{' (truncated)' if r['truncated'] else ''} | "
                   f"**Quotes verified**: {r['quotes_ok']}/{r['quotes_total']}\n"
                   f"- **Tags**: {', '.join(d['tags'])} | **Taxonomy**: " + " > ".join(d['taxonomy'].values()) + "\n")
        out.append("**Summary**\n" + "\n".join(f"{i}. {l}" for i, l in enumerate(d["summary_lines"], 1)) + "\n")
        out.append(f"**Insight**: {d['insight']}\n\n**Recommended action**: {d['recommended_action']}\n")
        out.append("**Key claims**\n" + "\n".join(
            f"- [{c['kind']}] {'✓' if c['quote_verified'] else '✗ QUOTE NOT FOUND'} {c['claim']}\n  > {c['evidence_quote']}"
            for c in d["key_claims"]) + "\n")
        if d["cve_ids"]:
            out.append(f"**CVE**: verified {d['cve_ids_verified']} | rejected {d['cve_ids_rejected']}\n")
        out.append(f"**Reliability notes**: {d['reliability_notes']}\n\n---\n")
    path = JSONL.parent / "sheets.md"
    path.write_text("\n".join(out))
    print(f"rendered -> {path}")


def cmd_review(args):
    con = connect()
    n = con.execute("UPDATE sheets SET review=? WHERE url LIKE ?", (args.status, args.url + "%")).rowcount
    con.execute("UPDATE prompt_log SET human_validation=? WHERE prompt_ref LIKE ?",
                (f"human review: {args.status}", f"%{args.url}%"))
    con.commit()
    print(f"{n} sheet(s) set to {args.status}")


def main():
    p = argparse.ArgumentParser(prog="veille")
    s = p.add_subparsers(required=True)
    c = s.add_parser("collect"); c.add_argument("--days", type=int, default=14); c.add_argument("--only", nargs="*"); c.set_defaults(f=cmd_collect)
    s.add_parser("rescore").set_defaults(f=cmd_rescore)
    s.add_parser("stats").set_defaults(f=cmd_stats)
    s.add_parser("export").set_defaults(f=cmd_export)
    sh = s.add_parser("sheet"); sh.add_argument("--top", type=int, default=5); sh.add_argument("--max-usd", type=float, default=1.0)
    sh.add_argument("--url", nargs="*"); sh.add_argument("--per-source", type=int, default=3); sh.set_defaults(f=cmd_sheet)
    s.add_parser("render").set_defaults(f=cmd_render)
    rv = s.add_parser("review"); rv.add_argument("url"); rv.add_argument("status", choices=["approved", "rejected", "draft"]); rv.set_defaults(f=cmd_review)
    s.add_parser("import").set_defaults(f=cmd_import)
    t = s.add_parser("top"); t.add_argument("-n", type=int, default=20); t.set_defaults(f=cmd_top)
    a = p.parse_args()
    a.f(a)
