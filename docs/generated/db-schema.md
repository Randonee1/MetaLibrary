# Database Schema

Generated summary of the current `library.sqlite` schema.

Current tables:

- `items`
- `papers`

## items

A stored physical file, content-addressed by `sha256`. The durable root entity.

```sql
CREATE TABLE items (
  id TEXT PRIMARY KEY,
  sha256 TEXT NOT NULL UNIQUE,
  size_bytes INTEGER NOT NULL,
  mime_type TEXT,
  storage_path TEXT NOT NULL UNIQUE,
  original_filename TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## papers

Bibliographic metadata for an item, generic across conference and journal
papers. One-to-one extension of `items` via a shared primary key.

```sql
CREATE TABLE papers (
  item_id TEXT PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  authors TEXT,            -- JSON array of author names
  abstract TEXT,
  issued_date TEXT,
  container_title TEXT,    -- journal name OR proceedings title
  volume TEXT,
  issue TEXT,
  pages TEXT,
  publisher TEXT,
  doi TEXT,
  url TEXT,
  extra TEXT               -- JSON catch-all (provenance, bibtex, etc.)
);
```

## Indexes

```sql
CREATE INDEX idx_items_sha256 ON items(sha256);
CREATE INDEX idx_papers_type ON papers(type);
CREATE INDEX idx_papers_title ON papers(title);
CREATE INDEX idx_papers_doi ON papers(doi);
CREATE INDEX idx_papers_url ON papers(url);
```

Schema changes must update this file.
