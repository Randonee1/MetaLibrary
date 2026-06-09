# Agent Guide

This repository is MetaLibrary, a local-first metadata and file storage system. It stores structured metadata in `library.sqlite` and original files under `storage/`.

Use this file as the map, not the manual. The source of truth lives in the docs below.

## Required Reading

- `ARCHITECTURE.md`: system boundaries, layer rules, and project scope.
- `docs/design/core-beliefs.md`: project principles.
- `docs/design/data-model.md`: database model and table ownership.
- `docs/design/storage-layout.md`: file storage rules.
- `docs/design/api-contract.md`: external API expectations.
- `docs/design/cli-contract.md`: command-line expectations.

## Working Rules

### Platform Boundary

- MetaLibrary is the generic platform for durable library storage, metadata, validation, identifiers, search, and public interfaces.
- `src/` contains MetaLibrary system code only. Do not place external applications, provider-specific workflows, or application-specific behavior under `src/`.
- Core and interface code must stay source-agnostic and application-agnostic. Narrow acquisition, collection, scraping, download, analysis, and reader workflows belong in `Applications/` or standalone `scripts/`.
- External clients, applications, and standalone scripts must not write directly to `library.sqlite` or `storage/`.
- Persistent data writes should go through MetaLibrary Core from inside platform interfaces, or through the public API/CLI from outside the platform.
- Dependency direction is platform-inward only: CLI/API may depend on Core; applications and standalone scripts should depend on API/CLI, not Core internals.

### Design Principles

- YAGNI: do not add tables, columns, modules, parameters, or abstractions without a current, stated requirement. When you drop something speculative, leave a clear upgrade path instead of building it now.
- No over-engineering: avoid speculative generality — extra abstraction layers, defensive code for impossible cases, and "might need it later" flexibility. Build the simplest thing that satisfies the actual requirement (KISS).
- DRY: each piece of knowledge has one authoritative home. Prefer a single source of truth over duplicated data or logic (e.g., structured columns over a redundant raw blob).
- Database design follows relational theory: choose structure by cardinality and functional dependency. Use a shared primary key for 1:1 extensions, a foreign key on the many side for 1:N, and a junction table for N:M only when that relationship is actually needed. Keep single-valued attributes as typed columns; use JSON only for multi-valued or open-ended data, never delimiter-packed values.
- These principles govern design choices, not baseline quality. Do not invoke them to skip tests, error handling, clear naming, or necessary constraints (foreign keys, UNIQUE, NOT NULL).

### Documentation And Checks

- After changing the database schema (`src/core/db.py`), run `scripts/check-schema` and resolve every reported violation. Adding a table also means updating its `EXPECTED_TABLES` allowlist and justifying the table in `docs/design/data-model.md`.
- Schema changes must update `docs/generated/db-schema.md`.
- Storage layout changes must update `docs/design/storage-layout.md`.
- API changes must update `docs/design/api-contract.md`.
- CLI changes must update `docs/design/cli-contract.md`.
- Run `scripts/check` before considering work complete.

## Current Project Shape

- `library.sqlite`: SQLite metadata database.
- `storage/`: original file storage.
- `src/`: MetaLibrary system implementation.
- `src/core/`: storage and database domain logic.
- `src/api/`: future HTTP API surface.
- `src/cli/`: command-line interface.
- `Applications/`: workspace for independent application repositories that consume MetaLibrary through API/CLI. Keep this directory itself empty until applications are added.
- `tests/`: unit and integration tests.
