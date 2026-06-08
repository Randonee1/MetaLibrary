# Storage Layout

Current layout:

```text
Library/
  library.sqlite
  storage/
```

`storage/` stores original files. The directory is system-managed and is not intended as a user browsing surface.

## Rules

- Store file paths in the database as paths relative to `Library/`.
- Do not use titles, authors, or publication dates as stable file identifiers.
- Do not write temporary or derived data into `storage/` unless the storage contract is updated.
- File writes should be atomic once Library Core is implemented.
- Every stored file should eventually have a checksum recorded in `blobs.sha256`.

## Future Options

The storage layout may evolve toward one of these patterns:

```text
storage/{attachment_key}/original.pdf
```

or:

```text
storage/blobs/{sha_prefix_1}/{sha_prefix_2}/{sha256}.pdf
```

Any migration must preserve database references and update this document.
