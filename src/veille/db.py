import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "veille.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id           INTEGER PRIMARY KEY,
    url          TEXT NOT NULL UNIQUE,
    title        TEXT NOT NULL,
    source       TEXT NOT NULL,
    source_type  TEXT NOT NULL,      -- primary / secondary / tertiary
    reliability  INTEGER NOT NULL,   -- 1..5 prior
    lang         TEXT NOT NULL,
    published    TEXT,               -- ISO 8601 UTC
    fetched_at   TEXT NOT NULL,
    summary      TEXT,
    score        INTEGER NOT NULL DEFAULT 0,
    matched      TEXT,               -- matched terms, comma separated
    relevant     INTEGER NOT NULL DEFAULT 0,
    status       TEXT NOT NULL DEFAULT 'new'   -- new / shortlisted / rejected / sheet_done
);
CREATE INDEX IF NOT EXISTS idx_articles_relevant ON articles(relevant, score DESC);
CREATE TABLE IF NOT EXISTS sheets (
    url          TEXT PRIMARY KEY REFERENCES articles(url),
    sheet        TEXT NOT NULL,      -- JSON produced by the model, enriched with verification results
    model        TEXT NOT NULL,
    created_at   TEXT NOT NULL,
    text_kind    TEXT NOT NULL,      -- full_text / stored_summary
    truncated    INTEGER NOT NULL DEFAULT 0,
    quotes_ok    INTEGER NOT NULL DEFAULT 0,
    quotes_total INTEGER NOT NULL DEFAULT 0,
    review       TEXT NOT NULL DEFAULT 'draft'   -- draft / approved / rejected (set by the human reviewer)
);
CREATE TABLE IF NOT EXISTS prompt_log (
    id INTEGER PRIMARY KEY, ts TEXT NOT NULL, phase TEXT NOT NULL, objective TEXT NOT NULL, model TEXT NOT NULL,
    prompt_ref TEXT NOT NULL,        -- which prompt template + article url
    input_tokens INTEGER, output_tokens INTEGER, cost_usd REAL, outcome TEXT, human_validation TEXT
);
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY, started_at TEXT, collector TEXT, fetched INTEGER, inserted INTEGER, error TEXT
);
"""


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    cols = {r["name"] for r in con.execute("PRAGMA table_info(sheets)")}
    if "ref" not in cols:  # stable citation key (S01, S02...) assigned when a sheet is approved
        con.execute("ALTER TABLE sheets ADD COLUMN ref TEXT")
        con.commit()
    return con
