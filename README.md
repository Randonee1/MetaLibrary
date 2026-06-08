# Library

Library is a local-first metadata and file storage system for papers, books, web pages, reports, and other readable or citable materials.

Current minimal layout:

```text
Library/
  library.sqlite
  storage/
  src/
  Applications/
```

The long-term goal is to provide a stable Library Core with HTTP API and CLI interfaces so external applications can read and write library data without depending on the internal SQLite schema or storage layout.

`src/` contains the Library system implementation. `Applications/` is a root-level workspace for many independent application repositories that use Library through API or CLI.

Run the project health check:

```bash
scripts/check
```

## First Version CLI

Create an item:

```bash
scripts/library item create --type journal_article --title "Example Paper"
```

Attach paper metadata:

```bash
scripts/library paper create ITEM_ID --publication-title "Example Journal" --doi "10.example/demo"
```

Add a file attachment:

```bash
scripts/library attachment add ITEM_ID /path/to/file.pdf
```

Search:

```bash
scripts/library search "keyword"
```
