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


def add_attachment(
    item_id: str,
    source_path: str | Path,
    *,
    title: str | None = None,
    attachment_type: str = "file",
    paths: LibraryPaths | None = None,
) -> dict[str, Any]:
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
        item = con.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if item is None:
            raise ValueError(f"item not found: {item_id}")

        blob = con.execute("SELECT * FROM blobs WHERE sha256 = ?", (digest,)).fetchone()
        if blob is None:
            blob_id = new_id("blob")
            dest_dir = paths.storage / blob_id
            dest_dir.mkdir(parents=True, exist_ok=False)
            filename = safe_filename(original_filename)
            dest = dest_dir / filename
            shutil.copy2(source, dest)
            storage_path = os.path.relpath(dest, paths.root)
            con.execute(
                """
                INSERT INTO blobs (id, sha256, mime_type, size_bytes, storage_path, original_filename)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (blob_id, digest, mime_type, size, storage_path, original_filename),
            )
            blob = con.execute("SELECT * FROM blobs WHERE id = ?", (blob_id,)).fetchone()

        attachment_id = new_id("att")
        con.execute(
            """
            INSERT INTO attachments (id, item_id, blob_id, attachment_type, title)
            VALUES (?, ?, ?, ?, ?)
            """,
            (attachment_id, item_id, blob["id"], attachment_type, title),
        )
        row = con.execute(
            """
            SELECT a.*, b.sha256, b.mime_type, b.size_bytes, b.storage_path, b.original_filename
            FROM attachments a
            JOIN blobs b ON b.id = a.blob_id
            WHERE a.id = ?
            """,
            (attachment_id,),
        ).fetchone()
    return row_to_dict(row) or {}


def list_attachments(item_id: str, paths: LibraryPaths | None = None) -> list[dict[str, Any]]:
    ensure_schema(paths)
    with connect(paths) as con:
        rows = con.execute(
            """
            SELECT a.*, b.sha256, b.mime_type, b.size_bytes, b.storage_path, b.original_filename
            FROM attachments a
            JOIN blobs b ON b.id = a.blob_id
            WHERE a.item_id = ?
            ORDER BY a.created_at, a.id
            """,
            (item_id,),
        ).fetchall()
    return [row_to_dict(row) or {} for row in rows]


def attachment_path(attachment_id: str, paths: LibraryPaths | None = None) -> Path | None:
    ensure_schema(paths)
    paths = paths or LibraryPaths.default()
    with connect(paths) as con:
        row = con.execute(
            """
            SELECT b.storage_path
            FROM attachments a
            JOIN blobs b ON b.id = a.blob_id
            WHERE a.id = ?
            """,
            (attachment_id,),
        ).fetchone()
    if row is None:
        return None
    return paths.root / row["storage_path"]
