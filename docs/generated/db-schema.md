# Database Schema

Generated summary of the current `library.sqlite` schema.

Current tables:

- `attachments`
- `blobs`
- `collection_items`
- `collections`
- `creators`
- `item_creators`
- `item_tags`
- `items`
- `papers`
- `tags`

First-version type-specific extension:

```sql
CREATE TABLE papers (
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
```

Schema changes must update this file.
