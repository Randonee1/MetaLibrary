from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from core.items import create_item, get_item
from core.papers import get_paper, upsert_paper
from core.paths import LibraryPaths
from core.search import search_items
from core.storage import add_attachment, attachment_path, list_attachments


class FirstVersionIntegrationTest(unittest.TestCase):
    def test_item_paper_attachment_and_search_flow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = LibraryPaths(root)
            source = root / "sample.pdf"
            source.write_bytes(b"%PDF-1.4 fixture\n")

            item = create_item(
                item_type="journal_article",
                title="Test Paper",
                abstract="A paper for testing",
                doi="10.0000/test",
                paths=paths,
            )
            self.assertEqual(item["title"], "Test Paper")

            paper = upsert_paper(
                item["id"],
                paths=paths,
                publication_title="Test Journal",
                published_date="2026",
                doi="10.0000/test",
            )
            self.assertEqual(paper["item_id"], item["id"])
            self.assertEqual(get_paper(item["id"], paths=paths)["publication_title"], "Test Journal")

            attachment = add_attachment(item["id"], source, title="Fixture PDF", paths=paths)
            self.assertEqual(attachment["item_id"], item["id"])
            self.assertTrue((root / attachment["storage_path"]).is_file())
            self.assertEqual(len(list_attachments(item["id"], paths=paths)), 1)
            self.assertTrue(attachment_path(attachment["id"], paths=paths).is_file())

            fetched = get_item(item["id"], paths=paths)
            self.assertEqual(fetched["paper"]["publication_title"], "Test Journal")
            self.assertEqual(len(fetched["attachments"]), 1)

            results = search_items("Test Paper", paths=paths)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["id"], item["id"])


if __name__ == "__main__":
    unittest.main()
