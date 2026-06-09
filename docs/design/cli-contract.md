# CLI Contract

The CLI is not implemented yet. This document defines the intended command shape.

Applications and automation scripts may use the CLI as a stable integration boundary when HTTP API access is not needed.

## Commands

```bash
scripts/library check
scripts/library db schema
scripts/library item add FILE
scripts/library item list
scripts/library item get ITEM_ID
scripts/library item path ITEM_ID
scripts/library paper create ITEM_ID [paper fields]
scripts/library paper get ITEM_ID
scripts/library paper find --url URL
scripts/library search QUERY
```

`paper find --url URL` returns the matching paper record, or an empty object
(exit 0) when none exists. Import tools use it to de-duplicate against the
database itself rather than an external manifest.

An item is a stored file: `item add FILE` ingests a file (deduplicated by
`sha256`) and returns the item id. `paper create` attaches bibliographic
metadata to that item. Paper fields are `--type` and `--title` (required on
create) plus `--authors --abstract --issued-date --container-title --volume --issue
--pages --publisher --doi --url --extra`.

## Rules

- CLI commands should call Library Core instead of duplicating database logic.
- Human-readable output is the default.
- Machine-readable JSON output should be available with `--json`.
- Import commands should report created item IDs.
