# CLI Contract

The CLI is not implemented yet. This document defines the intended command shape.

Applications and automation scripts may use the CLI as a stable integration boundary when HTTP API access is not needed.

## Planned Commands

```bash
scripts/library check
scripts/library db schema
scripts/library item create --type TYPE --title TITLE
scripts/library item list
scripts/library item get ITEM_ID
scripts/library paper create ITEM_ID [paper fields]
scripts/library paper get ITEM_ID
scripts/library attachment add ITEM_ID FILE
scripts/library attachment list ITEM_ID
scripts/library attachment path ATTACHMENT_ID
scripts/library search QUERY
```

## Rules

- CLI commands should call Library Core instead of duplicating database logic.
- Human-readable output is the default.
- Machine-readable JSON output should be available with `--json`.
- Import commands should report created item IDs and attachment IDs.
