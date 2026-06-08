# Agent Guide

This repository is a local-first library storage system. It stores structured metadata in `library.sqlite` and original files under `storage/`.

Use this file as the map, not the manual. The source of truth lives in `docs/`.

## Required Reading

- `ARCHITECTURE.md`: system boundaries and layer rules.
- `docs/design/core-beliefs.md`: project principles.
- `docs/design/data-model.md`: database model and table ownership.
- `docs/design/storage-layout.md`: file storage rules.
- `docs/design/api-contract.md`: external API expectations.
- `docs/design/cli-contract.md`: command-line expectations.

## Working Rules

- External applications must not write directly to `library.sqlite` or `storage/`.
- Data writes should go through Library Core, API, or CLI interfaces.
- Schema changes must update `docs/generated/db-schema.md`.
- Storage layout changes must update `docs/design/storage-layout.md`.
- API changes must update `docs/design/api-contract.md`.
- CLI changes must update `docs/design/cli-contract.md`.
- Run `scripts/check` before considering work complete.

## Current Project Shape

- `library.sqlite`: SQLite metadata database.
- `storage/`: original file storage.
- `src/core/`: storage and database domain logic.
- `src/api/`: future HTTP API surface.
- `src/cli/`: future command-line interface.
- `Applications/`: workspace for many independent application repositories that consume Library through API/CLI. Keep this directory itself empty until applications are added.
- `tests/`: unit and integration tests.
