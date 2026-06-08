# Architecture

MetaLibrary is a local storage platform for references, books, papers, web pages, and other readable or citable items.

MetaLibrary itself is the generic platform. The repository root contains the platform implementation, documentation, verification scripts, and a workspace for independent clients. `src/` is the MetaLibrary system code directory; it is not a place for external applications or source-specific workflows.

## Scope Boundary

MetaLibrary provides durable storage, metadata records, validation, identifiers, search, and public interfaces for reading and writing library data.

MetaLibrary should not encode narrow acquisition workflows, source-specific crawlers, provider-specific download logic, or application-specific behavior in the platform implementation. Those workflows belong in independent applications under `Applications/` or in standalone scripts under `scripts/`, and they should use the public API or CLI boundary for persistent writes.

## Layers

The system has three platform layers:

1. Core
   Owns the database schema, file storage, identifiers, validation, transactions, and generic domain operations.

2. Interfaces
   Exposes Core through HTTP API and CLI commands. External clients should use these interfaces instead of touching SQLite or files directly.

3. Applications
   Independent readers, analyzers, collectors, search tools, and other clients that consume MetaLibrary through API or CLI.

## Dependency Direction

Allowed direction:

```text
cli  -> core
api  -> core
applications -> API/CLI
scripts -> API/CLI
```

Disallowed direction:

```text
core -> api
core -> cli
applications -> direct SQLite/storage writes
scripts -> direct SQLite/storage writes
applications -> core internals
scripts -> core internals
```

## Source Layout

`src/` contains the MetaLibrary system implementation: core logic, API surface, and CLI surface.

`Applications/` lives at the repository root and is reserved for independent applications that consume MetaLibrary. Applications should not be placed under `src/` because they are clients of the platform, not part of the platform implementation.

Each child directory under `Applications/` may be its own Git repository, dependency graph, test suite, and release unit. The MetaLibrary repository ignores `Applications/*` from the root `.gitignore`, so application repositories remain separate from the MetaLibrary platform repository. Do not put placeholder files inside `Applications/` unless a real application is being added.

## Storage Boundary

The database stores metadata and relationships. `storage/` stores original files. Database rows reference files by relative storage paths.

The current storage layout is intentionally minimal:

```text
MetaLibrary/
  library.sqlite
  storage/
```

## Database Boundary

`items` is the universal root entity. Type-specific tables such as `papers` or `books` should reference `items.id` as their primary key and foreign key.

Attachments belong to `items`, not directly to type-specific tables.
