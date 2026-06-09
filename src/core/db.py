from __future__ import annotations

import sqlite3
from pathlib import Path

from .paths import LibraryPaths

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

-- An item uniquely identifies one stored physical file in MetaLibrary.
-- It is the durable, content-addressed root that metadata extensions hang off.
CREATE TABLE IF NOT EXISTS items (
  id TEXT PRIMARY KEY,
  sha256 TEXT NOT NULL UNIQUE,
  size_bytes INTEGER NOT NULL,
  mime_type TEXT,
  storage_path TEXT NOT NULL UNIQUE,
  original_filename TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Bibliographic record for an item, generic across conference and journal papers.
-- Shared primary key (item_id) gives a 1:1 extension of items.
CREATE TABLE IF NOT EXISTS papers (
  item_id TEXT PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  authors TEXT,
  abstract TEXT,
  issued_date TEXT,
  container_title TEXT,
  volume TEXT,
  issue TEXT,
  pages TEXT,
  publisher TEXT,
  doi TEXT,
  url TEXT,
  extra TEXT
);

CREATE INDEX IF NOT EXISTS idx_items_sha256 ON items(sha256);
CREATE INDEX IF NOT EXISTS idx_papers_type ON papers(type);
CREATE INDEX IF NOT EXISTS idx_papers_title ON papers(title);
CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi);
CREATE INDEX IF NOT EXISTS idx_papers_url ON papers(url);
"""


def connect(paths: LibraryPaths | None = None) -> sqlite3.Connection:
    paths = paths or LibraryPaths.default()
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.storage.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(paths.db)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def ensure_schema(paths: LibraryPaths | None = None) -> None:
    with connect(paths) as con:
        con.executescript(SCHEMA_SQL)


def table_names(paths: LibraryPaths | None = None) -> list[str]:
    with connect(paths) as con:
        return [
            row["name"]
            for row in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
        ]


def schema_for(paths: LibraryPaths | None = None) -> str:
    with connect(paths) as con:
        rows = con.execute(
            "SELECT sql FROM sqlite_master WHERE type IN ('table', 'index') AND sql IS NOT NULL ORDER BY type, name"
        ).fetchall()
    return "\n\n".join(row["sql"] for row in rows)
