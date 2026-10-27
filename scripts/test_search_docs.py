
"""Automated tests for the documentation search tool."""

import tempfile
import unittest
from pathlib import Path

from search_docs import load_articles, search_articles


class SearchDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs_dir = Path(self.temp_dir.name)

        (self.docs_dir / "account-access.md").write_text(
            "---\n"
            'title: "Account Access"\n'
            "---\n"
            "# Account Access\n"
            "Contact the administrator if account access is denied.\n",
            encoding="utf-8",
        )

        (self.docs_dir / "password-reset.md").write_text(
            "---\n"
            'title: "Password Reset"\n'
            "---\n"
            "# Password Reset\n"
            "Use the password reset process to create a new password.\n",
            encoding="utf-8",
        )

        self.articles = load_articles(self.docs_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_loads_markdown_articles(self):
        self.assertEqual(len(self.articles), 2)

    def test_finds_relevant_article(self):
        results = search_articles("reset password", self.articles)
        self.assertTrue(results)
        self.assertEqual(results[0][1]["title"], "Password Reset")

    def test_returns_no_results_for_unrelated_query(self):
        results = search_articles("spaceship maintenance", self.articles)
        self.assertEqual(results, [])

    def test_respects_result_limit(self):
        results = search_articles("account password access reset", self.articles, limit=1)
        self.assertLessEqual(len(results), 1)

    def test_empty_query_returns_no_results(self):
        results = search_articles("the and is", self.articles)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
