from __future__ import annotations

import json
from sqlite3 import Row
from typing import Any


def row_to_dict(row: Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def dump(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
