from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from core.items import add_item, get_item, item_path, list_items
from core.papers import find_paper_by_url, get_paper, upsert_paper
from core.paths import LibraryPaths
from core.search import search_items


class FirstVersionIntegrationTest(unittest.TestCase):
    def test_item_paper_and_search_flow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = LibraryPaths(root)
            source = root / "sample.pdf"
            source.write_bytes(b"%PDF-1.4 fixture\n")

            # An item *is* the stored file.
            item = add_item(source, paths=paths)
            item_id = item["id"]
            self.assertTrue((root / item["storage_path"]).is_file())
            self.assertEqual(item["original_filename"], "sample.pdf")
            self.assertEqual(item_path(item_id, paths=paths), root / item["storage_path"])

            # Re-adding the same content is idempotent (deduplicated by sha256).
            again = add_item(source, paths=paths)
            self.assertEqual(again["id"], item_id)
            self.assertEqual(len(list_items(paths=paths)), 1)

            paper = upsert_paper(
                item_id,
                paths=paths,
                type="conference_paper",
                title="Test Paper",
                authors=json.dumps(["Doe, J.", "Roe, R."]),
                issued_date="2026",
                container_title="Proceedings of the Test Conference",
                doi="10.0000/test",
            )
            self.assertEqual(paper["item_id"], item_id)
            self.assertEqual(get_paper(item_id, paths=paths)["title"], "Test Paper")

            # Partial update must not wipe other fields.
            upsert_paper(item_id, paths=paths, pages="1-10")
            updated = get_paper(item_id, paths=paths)
            self.assertEqual(updated["pages"], "1-10")
            self.assertEqual(updated["title"], "Test Paper")

            fetched = get_item(item_id, paths=paths)
            self.assertEqual(fetched["paper"]["container_title"], "Proceedings of the Test Conference")

            results = search_items("Test Paper", paths=paths)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["id"], item_id)

    def test_find_paper_by_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = LibraryPaths(root)
            source = root / "sample.pdf"
            source.write_bytes(b"%PDF-1.4 fixture\n")
            item = add_item(source, paths=paths)
            url = "https://example.org/paper.html"
            self.assertIsNone(find_paper_by_url(url, paths=paths))
            upsert_paper(item["id"], paths=paths, type="conference_paper", title="T", url=url)
            found = find_paper_by_url(url, paths=paths)
            self.assertIsNotNone(found)
            self.assertEqual(found["item_id"], item["id"])

    def test_paper_requires_type_and_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = LibraryPaths(root)
            source = root / "sample.pdf"
            source.write_bytes(b"%PDF-1.4 fixture\n")
            item = add_item(source, paths=paths)
            with self.assertRaises(ValueError):
                upsert_paper(item["id"], paths=paths, title="No Type")


if __name__ == "__main__":
    unittest.main()
