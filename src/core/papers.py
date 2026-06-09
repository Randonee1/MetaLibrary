from __future__ import annotations

from typing import Any

from .db import connect, ensure_schema
from .paths import LibraryPaths
from .records import row_to_dict

PAPER_FIELDS = [
    "type",
    "title",
    "authors",
    "abstract",
    "issued_date",
    "container_title",
    "volume",
    "issue",
    "pages",
    "publisher",
    "doi",
    "url",
    "extra",
]

REQUIRED_FIELDS = ("type", "title")


def upsert_paper(item_id: str, paths: LibraryPaths | None = None, **fields: str | None) -> dict[str, Any]:
    ensure_schema(paths)
    provided = {field: fields.get(field) for field in PAPER_FIELDS if fields.get(field) is not None}
    with connect(paths) as con:
        item = con.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if item is None:
            raise ValueError(f"item not found: {item_id}")
        existing = con.execute("SELECT item_id FROM papers WHERE item_id = ?", (item_id,)).fetchone()
        if existing:
            if provided:
                assignments = ", ".join(f"{field} = ?" for field in provided)
                con.execute(
                    f"UPDATE papers SET {assignments} WHERE item_id = ?",
                    (*provided.values(), item_id),
                )
        else:
            missing = [field for field in REQUIRED_FIELDS if not provided.get(field)]
            if missing:
                raise ValueError(f"missing required paper fields: {', '.join(missing)}")
            columns = ["item_id", *provided.keys()]
            placeholders = ", ".join("?" for _ in columns)
            con.execute(
                f"INSERT INTO papers ({', '.join(columns)}) VALUES ({placeholders})",
                (item_id, *provided.values()),
            )
        row = con.execute("SELECT * FROM papers WHERE item_id = ?", (item_id,)).fetchone()
    return row_to_dict(row) or {}


def get_paper(item_id: str, paths: LibraryPaths | None = None) -> dict[str, Any] | None:
    ensure_schema(paths)
    with connect(paths) as con:
        row = con.execute("SELECT * FROM papers WHERE item_id = ?", (item_id,)).fetchone()
    return row_to_dict(row)


def find_paper_by_url(url: str, paths: LibraryPaths | None = None) -> dict[str, Any] | None:
    """Look up an existing paper by its source URL (used for import de-duplication)."""
    ensure_schema(paths)
    with connect(paths) as con:
        row = con.execute("SELECT * FROM papers WHERE url = ?", (url,)).fetchone()
    return row_to_dict(row)
