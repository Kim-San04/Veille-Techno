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
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY, started_at TEXT, collector TEXT, fetched INTEGER, inserted INTEGER, error TEXT
);
"""


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con
