from __future__ import annotations

from typing import Any

from .db import connect, ensure_schema
from .records import row_to_dict
from .paths import LibraryPaths

PAPER_FIELDS = [
    "publication_title",
    "journal_abbreviation",
    "publisher",
    "published_date",
    "volume",
    "issue",
    "pages",
    "doi",
    "pmid",
    "pmcid",
    "issn",
    "citation_key",
    "access_date",
    "extra",
]


def upsert_paper(item_id: str, paths: LibraryPaths | None = None, **fields: str | None) -> dict[str, Any]:
    ensure_schema(paths)
    values = {field: fields.get(field) for field in PAPER_FIELDS}
    with connect(paths) as con:
        item = con.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if item is None:
            raise ValueError(f"item not found: {item_id}")
        existing = con.execute("SELECT item_id FROM papers WHERE item_id = ?", (item_id,)).fetchone()
        if existing:
            assignments = ", ".join(f"{field} = ?" for field in PAPER_FIELDS)
            con.execute(
                f"UPDATE papers SET {assignments}, updated_at = CURRENT_TIMESTAMP WHERE item_id = ?",
                (*[values[field] for field in PAPER_FIELDS], item_id),
            )
        else:
            columns = ", ".join(["item_id", *PAPER_FIELDS])
            placeholders = ", ".join("?" for _ in ["item_id", *PAPER_FIELDS])
            con.execute(
                f"INSERT INTO papers ({columns}) VALUES ({placeholders})",
                (item_id, *[values[field] for field in PAPER_FIELDS]),
            )
        row = con.execute("SELECT * FROM papers WHERE item_id = ?", (item_id,)).fetchone()
    return row_to_dict(row) or {}


def get_paper(item_id: str, paths: LibraryPaths | None = None) -> dict[str, Any] | None:
    ensure_schema(paths)
    with connect(paths) as con:
        row = con.execute("SELECT * FROM papers WHERE item_id = ?", (item_id,)).fetchone()
    return row_to_dict(row)
