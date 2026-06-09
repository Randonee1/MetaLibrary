from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import shutil
from pathlib import Path
from typing import Any

from .db import connect, ensure_schema
from .ids import new_id
from .paths import LibraryPaths
from .records import row_to_dict

_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_filename(name: str) -> str:
    cleaned = _SAFE_NAME.sub("_", name).strip("._")
    return cleaned or "file"


def add_item(source_path: str | Path, paths: LibraryPaths | None = None) -> dict[str, Any]:
    """Ingest a file as an item.

    An item *is* the stored file: its identity is the content hash. Importing the
    same file twice is idempotent and returns the existing item rather than
    duplicating storage.
    """
    ensure_schema(paths)
    paths = paths or LibraryPaths.default()
    source = Path(source_path).expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"not a file: {source}")

    digest = sha256_file(source)
    size = source.stat().st_size
    mime_type = mimetypes.guess_type(source.name)[0]
    original_filename = source.name

    with connect(paths) as con:
        existing = con.execute("SELECT * FROM items WHERE sha256 = ?", (digest,)).fetchone()
        if existing is not None:
            return row_to_dict(existing) or {}

        item_id = new_id("item")
        dest_dir = paths.storage / item_id
        dest_dir.mkdir(parents=True, exist_ok=False)
        dest = dest_dir / safe_filename(original_filename)
        shutil.copy2(source, dest)
        storage_path = os.path.relpath(dest, paths.root)
        con.execute(
            """
            INSERT INTO items (id, sha256, size_bytes, mime_type, storage_path, original_filename)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (item_id, digest, size, mime_type, storage_path, original_filename),
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
    item["paper"] = paper
    return item


def list_items(limit: int = 50, paths: LibraryPaths | None = None) -> list[dict[str, Any]]:
    ensure_schema(paths)
    with connect(paths) as con:
        rows = con.execute(
            """
            SELECT i.*, p.type AS paper_type, p.title AS paper_title
            FROM items i
            LEFT JOIN papers p ON p.item_id = i.id
            ORDER BY i.created_at DESC, i.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [row_to_dict(row) or {} for row in rows]


def item_path(item_id: str, paths: LibraryPaths | None = None) -> Path | None:
    ensure_schema(paths)
    paths = paths or LibraryPaths.default()
    with connect(paths) as con:
        row = con.execute("SELECT storage_path FROM items WHERE id = ?", (item_id,)).fetchone()
    if row is None:
        return None
    return paths.root / row["storage_path"]
