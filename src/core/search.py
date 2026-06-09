from __future__ import annotations

from typing import Any

from .db import connect, ensure_schema
from .paths import LibraryPaths
from .records import row_to_dict


def search_items(query: str, limit: int = 50, paths: LibraryPaths | None = None) -> list[dict[str, Any]]:
    ensure_schema(paths)
    pattern = f"%{query}%"
    with connect(paths) as con:
        rows = con.execute(
            """
            SELECT i.id, i.storage_path, i.original_filename,
                   p.type, p.title, p.authors, p.container_title, p.doi
            FROM items i
            JOIN papers p ON p.item_id = i.id
            WHERE p.title LIKE ?
               OR p.authors LIKE ?
               OR p.container_title LIKE ?
               OR p.doi LIKE ?
            ORDER BY i.created_at DESC, i.id DESC
            LIMIT ?
            """,
            (pattern, pattern, pattern, pattern, limit),
        ).fetchall()
    return [row_to_dict(row) or {} for row in rows]
