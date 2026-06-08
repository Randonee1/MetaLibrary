from __future__ import annotations

from typing import Any

from .db import connect, ensure_schema
from .ids import new_id
from .paths import LibraryPaths
from .records import row_to_dict


def create_item(
    *,
    item_type: str,
    title: str,
    abstract: str | None = None,
    language: str | None = None,
    date: str | None = None,
    url: str | None = None,
    doi: str | None = None,
    isbn: str | None = None,
    paths: LibraryPaths | None = None,
) -> dict[str, Any]:
    ensure_schema(paths)
    item_id = new_id("item")
    with connect(paths) as con:
        con.execute(
            """
            INSERT INTO items (id, item_type, title, abstract, language, date, url, doi, isbn)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (item_id, item_type, title, abstract, language, date, url, doi, isbn),
        )
        row = con.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    return row_to_dict(row) or {}


def get_item(item_id: str, paths: LibraryPaths | None = None) -> dict[str, Any] | None:
    ensure_schema(paths)
    with connect(paths) as con:
        item = row_to_dict(con.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone())
        if not item:
            return None
        paper = row_to_dict(con.execute("SELECT * FROM papers WHERE item_id = ?", (item_id,)).fetchone())
        attachments = [
            row_to_dict(row)
            for row in con.execute(
                """
                SELECT a.*, b.sha256, b.mime_type, b.size_bytes, b.storage_path, b.original_filename
                FROM attachments a
                JOIN blobs b ON b.id = a.blob_id
                WHERE a.item_id = ?
                ORDER BY a.created_at, a.id
                """,
                (item_id,),
            )
        ]
    item["paper"] = paper
    item["attachments"] = attachments
    return item


def list_items(limit: int = 50, paths: LibraryPaths | None = None) -> list[dict[str, Any]]:
    ensure_schema(paths)
    with connect(paths) as con:
        rows = con.execute(
            "SELECT * FROM items ORDER BY created_at DESC, id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [row_to_dict(row) or {} for row in rows]
