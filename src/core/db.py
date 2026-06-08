from __future__ import annotations

import sqlite3
from pathlib import Path

from .paths import LibraryPaths

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items (
  id TEXT PRIMARY KEY,
  item_type TEXT NOT NULL,
  title TEXT NOT NULL,
  abstract TEXT,
  language TEXT,
  date TEXT,
  url TEXT,
  doi TEXT,
  isbn TEXT,
  extra_json TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS papers (
  item_id TEXT PRIMARY KEY,
  publication_title TEXT,
  journal_abbreviation TEXT,
  publisher TEXT,
  published_date TEXT,
  volume TEXT,
  issue TEXT,
  pages TEXT,
  doi TEXT,
  pmid TEXT,
  pmcid TEXT,
  issn TEXT,
  citation_key TEXT,
  access_date TEXT,
  extra TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS creators (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  given_name TEXT,
  family_name TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS item_creators (
  item_id TEXT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  creator_id TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
  role TEXT NOT NULL,
  position INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (item_id, creator_id, role)
);

CREATE TABLE IF NOT EXISTS blobs (
  id TEXT PRIMARY KEY,
  sha256 TEXT NOT NULL UNIQUE,
  mime_type TEXT,
  size_bytes INTEGER NOT NULL,
  storage_path TEXT NOT NULL UNIQUE,
  original_filename TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attachments (
  id TEXT PRIMARY KEY,
  item_id TEXT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  blob_id TEXT NOT NULL REFERENCES blobs(id) ON DELETE RESTRICT,
  attachment_type TEXT NOT NULL DEFAULT 'file',
  title TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS item_tags (
  item_id TEXT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  tag_id TEXT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (item_id, tag_id)
);

CREATE TABLE IF NOT EXISTS collections (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  parent_id TEXT REFERENCES collections(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS collection_items (
  collection_id TEXT NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
  item_id TEXT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  PRIMARY KEY (collection_id, item_id)
);

CREATE INDEX IF NOT EXISTS idx_items_type ON items(item_type);
CREATE INDEX IF NOT EXISTS idx_items_title ON items(title);
CREATE INDEX IF NOT EXISTS idx_items_doi ON items(doi);
CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi);
CREATE INDEX IF NOT EXISTS idx_papers_publication_title ON papers(publication_title);
CREATE INDEX IF NOT EXISTS idx_attachments_item ON attachments(item_id);
CREATE INDEX IF NOT EXISTS idx_blobs_sha256 ON blobs(sha256);
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
