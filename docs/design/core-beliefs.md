# Core Beliefs

## Local First

The library must remain useful without a network connection. Remote metadata services can enrich data, but local data remains authoritative.

## Interfaces Over Internals

External applications should interact through API or CLI interfaces. Direct writes to `library.sqlite` and `storage/` are reserved for Library Core.

## Platform And Applications Are Separate

Library Core is the platform. Applications are clients of the platform and belong as independent repositories under the root-level `Applications/` workspace, not under `src/`.

## Stable Core, Extensible Edges

Core tables should stay small and stable. Type-specific or application-specific data belongs in extension tables.

## Original Files Are Durable

Files in `storage/` are original inputs and should not be casually deleted or rewritten. Derived data can be regenerated later and should not be mixed into the minimal storage contract until needed.

## Mechanical Verification

Project rules should be enforced by scripts, tests, schema checks, and generated documentation where possible.
