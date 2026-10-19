import re
import time
from datetime import datetime, timedelta, timezone
from html import unescape
from time import struct_time
from calendar import timegm

import feedparser
import requests

UA = {"User-Agent": "veille-bot/0.1 (student monitoring project)"}
TAG = re.compile(r"<[^>]+>")


def clean(text: str | None, limit: int = 1500) -> str:
    return re.sub(r"\s+", " ", unescape(TAG.sub(" ", text or ""))).strip()[:limit]


def iso(t: struct_time | None) -> str | None:
    if not t or t.tm_year < 2000:  # some feeds ship placeholder dates (year 0001)
        return None
    return datetime.fromtimestamp(timegm(t), timezone.utc).isoformat()


def item(url, title, published, summary, meta):
    return {"url": url, "title": clean(title, 300), "published": published,
            "summary": clean(summary), "source": meta["name"], "type": meta["type"],
            "reliability": meta["reliability"], "lang": meta["lang"]}


def rss(meta: dict) -> list[dict]:
    r = requests.get(meta["url"], timeout=30, headers=UA)
    r.raise_for_status()
    feed = feedparser.parse(r.content)
    return [item(e.get("link"), e.get("title"), iso(e.get("published_parsed") or e.get("updated_parsed")),
                 e.get("summary") or (e.get("content") or [{}])[0].get("value"), meta)
            for e in feed.entries if e.get("link")]


def nvd(meta: dict, queries: list[str], since: datetime) -> list[dict]:
    out = []
    fmt = "%Y-%m-%dT%H:%M:%S.000"
    for q in queries:
        params = {"keywordSearch": q, "resultsPerPage": 50,
                  "lastModStartDate": since.strftime(fmt), "lastModEndDate": datetime.now(timezone.utc).strftime(fmt)}
        r = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0", params=params, timeout=60, headers=UA)
        if r.status_code == 200:
            for v in r.json().get("vulnerabilities", []):
                c = v["cve"]
                desc = next((d["value"] for d in c.get("descriptions", []) if d["lang"] == "en"), "")
                out.append(item(f"https://nvd.nist.gov/vuln/detail/{c['id']}", f"{c['id']}: {desc[:120]}",
                                c.get("published"), desc, meta))
        time.sleep(7)  # NVD public rate limit: 5 requests / 30 s without an API key
    return out


def arxiv(meta: dict, queries: list[str]) -> list[dict]:
    out = []
    for q in queries:
        r = requests.get("http://export.arxiv.org/api/query", headers=UA, timeout=60,
                         params={"search_query": f"cat:cs.CR AND ({q})", "sortBy": "submittedDate", "max_results": 25})
        r.raise_for_status()
        for e in feedparser.parse(r.content).entries:
            out.append(item(e.link, e.title, iso(e.get("published_parsed")), e.get("summary"), meta))
        time.sleep(3)  # arXiv asks for >= 3 s between calls
    return out


def hn(meta: dict, queries: list[str], since: datetime) -> list[dict]:
    out = []
    for q in queries:
        r = requests.get("https://hn.algolia.com/api/v1/search_by_date", timeout=30, headers=UA,
                         params={"query": q, "tags": "story", "hitsPerPage": 30,
                                 "numericFilters": f"created_at_i>{int(since.timestamp())},points>10"})
        r.raise_for_status()
        for h in r.json()["hits"]:
            if h.get("url"):
                out.append(item(h["url"], h["title"], h["created_at"], f"HN points: {h.get('points')} — {h['title']}", meta))
    return out


def ghsa(meta: dict, terms: list[str]) -> list[dict]:
    r = requests.get("https://api.github.com/advisories", params={"per_page": 100}, timeout=30,
                     headers={**UA, "Accept": "application/vnd.github+json"})
    r.raise_for_status()
    out = []
    for a in r.json():
        text = f"{a.get('summary','')} {a.get('description') or ''}".lower()
        if any(t in text for t in terms):
            out.append(item(a["html_url"], f"{a['ghsa_id']}: {a['summary']}", a.get("published_at"),
                            a.get("description"), meta))
    return out


def gnews(meta: dict, queries: list[str]) -> list[dict]:
    """Google News RSS (French edition). Links are Google redirects: usable for discovery and dedup,
    the real publisher is appended to the title ("... - Publisher")."""
    from urllib.parse import quote
    out = []
    for q in queries:
        url = f"https://news.google.com/rss/search?q={quote(q)}&hl=fr&gl=FR&ceid=FR:fr"
        r = requests.get(url, timeout=30, headers=UA)
        r.raise_for_status()
        for e in feedparser.parse(r.content).entries:
            pub = (e.get("source") or {}).get("title") or ""
            title = e.get("title", "")
            m = {**meta, "name": f"GN · {pub}" if pub else meta["name"]}
            out.append(item(e.link, title, iso(e.get("published_parsed")), e.get("summary") or title, m))
        time.sleep(2)
    return out
