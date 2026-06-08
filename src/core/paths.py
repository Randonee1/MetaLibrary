from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LibraryPaths:
    root: Path

    @classmethod
    def default(cls) -> "LibraryPaths":
        return cls(Path(__file__).resolve().parents[2])

    @property
    def db(self) -> Path:
        return self.root / "library.sqlite"

    @property
    def storage(self) -> Path:
        return self.root / "storage"
