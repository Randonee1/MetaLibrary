# Data Model

The current database uses SQLite at `library.sqlite`.

The model is intentionally minimal: only tables backed by a current requirement
exist. Relationships that are not yet needed (authors-as-entities, tags,
collections) are deliberately omitted and can be introduced later as real
requirements appear.

## Core Entities

- `items`: a stored physical file. Each row uniquely identifies one file in
  MetaLibrary, content-addressed by `sha256`. This is the durable root entity.
- `papers`: bibliographic metadata describing an item, generic across
  conference and journal papers. One-to-one extension of `items`.

> Note on naming: `items` here means *the stored file*, not the Zotero-style
> bibliographic record. The bibliographic record lives in `papers`.

## Extension Pattern

A type-specific table extends `items` using `item_id` as **both primary key and
foreign key** (shared primary key), giving a one-to-one extension:

```sql
CREATE TABLE papers (
  item_id TEXT PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  ...
);
```

A paper is an item (file) with paper-specific descriptive fields. No separate
surrogate id is added: the 1:1 cardinality and existence dependency make the
owner's key the natural identifier.

## Field Conventions

- **Single-valued attributes** are their own typed columns (queryable,
  indexable, constrainable): `title`, `doi`, `volume`, `pages`, etc.
- **Multi-valued attributes** use JSON until a relational requirement appears.
  `authors` is a JSON array of names. When author-level search or de-duplication
  is needed, migrate to normalized `creators` + `item_creators` tables.
- **Venue is unified**: one `container_title` holds the journal name *or* the
  proceedings title (CSL `container-title`), rather than separate columns per
  type.
- **`extra`** is a JSON catch-all for provenance and fields without a dedicated
  column (e.g. original BibTeX, source URLs, conference name, ISSN).

## Ownership

- File identity (hash, size, MIME, storage path) belongs in `items`.
- Descriptive metadata (title, authors, abstract, venue, identifiers) belongs in `papers`.
- `created_at` (ingestion time) lives on `items`. There is no `updated_at` until
  a feature needs last-modified tracking; if added, it belongs on `papers` (the
  mutable side), not `items` (the immutable file).

## First Version Implementation

The first implementation provides Library Core and CLI commands for:

- ingesting files as `items`, deduplicated by `sha256`, stored under
  `storage/{item_id}/{filename}`;
- creating or updating `papers` rows linked by `papers.item_id`;
- fetching an item together with its paper record;
- searching common paper fields (title, authors, venue, DOI).
