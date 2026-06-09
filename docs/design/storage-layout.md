# Storage Layout

Current layout:

```text
Library/
  library.sqlite
  storage/
```

`storage/` stores original files. The directory is system-managed and is not intended as a user browsing surface.

Each ingested file is stored under a per-item directory:

```text
storage/{item_id}/{original_filename}
```

## Rules

- Store file paths in the database as paths relative to `Library/` (`items.storage_path`).
- Do not use titles, authors, or publication dates as stable file identifiers.
- Do not write temporary or derived data into `storage/` unless the storage contract is updated.
- Every stored file has its checksum recorded in `items.sha256`; identical content is deduplicated to a single item.

## Future Options

The storage layout may evolve toward a content-addressed pattern:

```text
storage/blobs/{sha_prefix_1}/{sha_prefix_2}/{sha256}.pdf
```

Any migration must preserve database references and update this document.
