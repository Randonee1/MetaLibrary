# Architecture

Library is a local storage platform for references, books, papers, web pages, and other readable or citable items.

The system has three layers:

1. Library Core
   Owns the database schema, file storage, identifiers, imports, validation, and transactions.

2. Interfaces
   Exposes Library Core through HTTP API and CLI commands. External applications should use these interfaces instead of touching SQLite or files directly.

3. Applications
   Readers, analyzers, collectors, search tools, and other clients that consume the Library interfaces.

## Dependency Direction

Allowed direction:

```text
cli  -> core
api  -> core
applications -> API/CLI
```

Disallowed direction:

```text
core -> api
core -> cli
applications -> direct SQLite/storage writes
```

## Source Layout

`src/` contains the Library system itself: core logic, API surface, and CLI surface. It is not a general workspace.

`Applications/` lives at the repository root and is reserved for many independent applications that consume Library. Applications should not be placed under `src/` because they are clients of the platform, not part of the platform implementation.

Each child directory under `Applications/` may be its own Git repository, dependency graph, test suite, and release unit. The Library repository ignores `Applications/*` from the root `.gitignore`, so application repositories remain separate from the Library platform repository. Do not put placeholder files inside `Applications/` unless a real application is being added.

## Storage Boundary

The database stores metadata and relationships. `storage/` stores original files. Database rows reference files by relative storage paths.

The current storage layout is intentionally minimal:

```text
Library/
  library.sqlite
  storage/
```

## Database Boundary

`items` is the universal root entity. Type-specific tables such as `papers` or `books` should reference `items.id` as their primary key and foreign key.

Attachments belong to `items`, not directly to type-specific tables.
