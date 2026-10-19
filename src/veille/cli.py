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
    for r in con.execute("SELECT id,title,summary FROM articles").fetchall():
        s, m, rel = matrix.score(r["title"], r["summary"])
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
    con.commit()
    print(f"imported {n} articles")


def main():
    p = argparse.ArgumentParser(prog="veille")
    s = p.add_subparsers(required=True)
    c = s.add_parser("collect"); c.add_argument("--days", type=int, default=14); c.add_argument("--only", nargs="*"); c.set_defaults(f=cmd_collect)
    s.add_parser("rescore").set_defaults(f=cmd_rescore)
    s.add_parser("stats").set_defaults(f=cmd_stats)
    s.add_parser("export").set_defaults(f=cmd_export)
    s.add_parser("import").set_defaults(f=cmd_import)
    t = s.add_parser("top"); t.add_argument("-n", type=int, default=20); t.set_defaults(f=cmd_top)
    a = p.parse_args()
    a.f(a)
