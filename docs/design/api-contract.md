# API Contract

The HTTP API is not implemented yet. This document defines the intended contract.

External applications should use API endpoints instead of directly writing `library.sqlite` or `storage/`.

Applications may live under `Applications/`, but they should still treat this API contract as their supported integration boundary.

## Planned Resources

- `GET /items`
- `POST /items` (upload a file; an item is a stored file)
- `GET /items/{item_id}`
- `GET /items/{item_id}/file`
- `DELETE /items/{item_id}`
- `PUT /items/{item_id}/paper` (create or update bibliographic metadata)
- `GET /items/{item_id}/paper`
- `POST /metadata/resolve`
- `GET /search`

## Boundary Rules

- Parse and validate request bodies at the boundary.
- Return stable JSON shapes.
- Do not expose SQLite internals as public API details.
- An uploaded file is recorded as one `items` row, deduplicated by `sha256`.
