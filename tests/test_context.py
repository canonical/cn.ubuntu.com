import unittest

from webapp.app import app
from webapp.context import modify_query


class TestModifyQuery(unittest.TestCase):
    """Tests for webapp.context.modify_query"""

    def test_adds_param_when_query_empty(self):
        with app.test_request_context("/engage"):
            result = modify_query({"page": 2})

        self.assertEqual(result, "page=2")

    def test_overrides_existing_param(self):
        with app.test_request_context("/engage?page=1"):
            result = modify_query({"page": 3})

        self.assertEqual(result, "page=3")

    def test_adds_param_alongside_existing(self):
        with app.test_request_context("/engage?topic=cloud"):
            result = modify_query({"page": 2})

        # parse_qs preserves both; order is insertion order
        self.assertIn("topic=cloud", result)
        self.assertIn("page=2", result)

    def test_updates_multiple_params(self):
        with app.test_request_context("/engage?page=1&topic=cloud"):
            result = modify_query({"page": 4, "sort": "newest"})

        self.assertIn("page=4", result)
        self.assertIn("topic=cloud", result)
        self.assertIn("sort=newest", result)
        self.assertNotIn("page=1", result)

    def test_preserves_blank_values(self):
        with app.test_request_context("/engage?topic="):
            result = modify_query({"page": 2})

        self.assertIn("topic=", result)
        self.assertIn("page=2", result)


if __name__ == "__main__":
    unittest.main()
