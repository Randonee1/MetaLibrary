# Zotero Reference

Zotero is the main reference for library data modeling.

Useful ideas:

- `items` as a universal root table.
- item types for journal articles, books, web pages, reports, theses, and more.
- separate creator tables with ordered creator relationships.
- separate attachment records and storage directories.
- tags and collections as organization primitives.

Do not copy Zotero's SQLite schema directly. Use it as a design reference.
