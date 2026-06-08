# API Contract

The HTTP API is not implemented yet. This document defines the intended contract.

External applications should use API endpoints instead of directly writing `library.sqlite` or `storage/`.

Applications may live under `Applications/`, but they should still treat this API contract as their supported integration boundary.

## Planned Resources

- `GET /items`
- `POST /items`
- `GET /items/{item_id}`
- `PATCH /items/{item_id}`
- `DELETE /items/{item_id}`
- `POST /items/{item_id}/attachments`
- `GET /items/{item_id}/attachments`
- `GET /attachments/{attachment_id}/file`
- `POST /import/file`
- `POST /metadata/resolve`
- `GET /search`

## Boundary Rules

- Parse and validate request bodies at the boundary.
- Return stable JSON shapes.
- Do not expose SQLite internals as public API details.
- File uploads must be recorded in both `blobs` and `attachments`.
