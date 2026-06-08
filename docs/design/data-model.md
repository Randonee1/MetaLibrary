# Data Model

The current database uses SQLite at `library.sqlite`.

## Core Entities

- `items`: universal metadata root for papers, books, reports, web pages, and other item types.
- `creators`: people or organizations related to an item.
- `item_creators`: ordered creator relationships, including roles such as author, editor, and translator.
- `blobs`: stored file records, including hash, size, MIME type, and storage path.
- `attachments`: relationship between an item and a stored blob.
- `tags` and `item_tags`: labels.
- `collections` and `collection_items`: user organization.

## Extension Pattern

Type-specific tables should use `item_id` as both primary key and foreign key:

```sql
CREATE TABLE papers (
  item_id TEXT PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
  publication_title TEXT,
  published_date TEXT,
  doi TEXT
);
```

This creates a one-to-one extension of `items`. A paper is an item with paper-specific fields.

## Ownership

- Common fields belong in `items`.
- Type-specific fields belong in tables such as `papers` or `books`.
- Authors and editors belong in `creators` and `item_creators`.
- Files belong in `blobs`; item-file relationships belong in `attachments`.
- Import provenance belongs in future metadata source tables.

## First Version Implementation

The first implementation provides Library Core and CLI commands for:

- creating and listing `items`;
- creating or updating `papers` rows linked by `papers.item_id`;
- importing file attachments into `storage/{blob_id}/{filename}`;
- deduplicating stored file blobs by `sha256`;
- searching common item and paper fields.
