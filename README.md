# MetaLibrary

MetaLibrary is a local-first metadata and file storage system for papers, books, web pages, reports, and other readable or citable materials.

Current minimal layout:

```text
MetaLibrary/
  library.sqlite
  storage/
  src/
  Applications/
```

The long-term goal is to provide a stable MetaLibrary Core with HTTP API and CLI interfaces so external applications can read and write library data without depending on the internal SQLite schema or storage layout.

`src/` contains the MetaLibrary system implementation. `Applications/` is a root-level workspace for independent application repositories that use MetaLibrary through API or CLI. Concrete acquisition and application workflows should live in `Applications/` or standalone scripts, and should use MetaLibrary public interfaces for persistent writes.

Run the project health check:

```bash
scripts/check
```

## First Version CLI

An item is a stored file. Ingest one (deduplicated by content hash):

```bash
scripts/library item add /path/to/file.pdf
```

Attach paper metadata to the returned item id:

```bash
scripts/library paper create ITEM_ID \
  --type conference_paper \
  --title "Example Paper" \
  --container-title "Proceedings of the Example Conference" \
  --doi "10.example/demo"
```

Inspect an item and its stored file path:

```bash
scripts/library item get ITEM_ID
scripts/library item path ITEM_ID
```

Search:

```bash
scripts/library search "keyword"
```
