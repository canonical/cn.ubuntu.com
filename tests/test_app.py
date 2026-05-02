import unittest

from webapp.app import app, localize_type, modify_query


class TestLocalizeTypeFilter(unittest.TestCase):
    """Tests for the localize_type Jinja template filter"""

    def test_known_types_return_chinese(self):
        cases = {
            "blog": "博客",
            "case study": "案例分享",
            "datasheet": "产品说明书",
            "event": "活动",
            "form": "表单",
            "guide": "指南",
            "roadshow": "活动",
            "whitepaper": "白皮书",
            "webinar": "网络研讨会",
        }
        for english, chinese in cases.items():
            with self.subTest(value=english):
                self.assertEqual(localize_type(english), chinese)

    def test_match_is_case_insensitive(self):
        self.assertEqual(localize_type("Blog"), "博客")
        self.assertEqual(localize_type("WHITEPAPER"), "白皮书")
        self.assertEqual(localize_type("Case Study"), "案例分享")

    def test_surrounding_whitespace_stripped(self):
        self.assertEqual(localize_type("  blog  "), "博客")
        self.assertEqual(localize_type("\tcase study\n"), "案例分享")

    def test_unknown_type_returned_unchanged(self):
        self.assertEqual(localize_type("podcast"), "podcast")
        self.assertEqual(localize_type("Tutorial"), "Tutorial")

    def test_empty_string_returned_unchanged(self):
        self.assertEqual(localize_type(""), "")

    def test_none_returned_unchanged(self):
        self.assertIsNone(localize_type(None))

    def test_filter_registered_on_app(self):
        self.assertIn("localize_type", app.jinja_env.filters)
        self.assertIs(app.jinja_env.filters["localize_type"], localize_type)


class TestTemplateContext(unittest.TestCase):
    """Tests for the @app.context_processor template context"""

    def test_modify_query_in_context(self):
        with app.test_request_context("/engage"):
            contexts = app.update_template_context({})

        self.assertIn("modify_query", contexts)
        self.assertIs(contexts["modify_query"], modify_query)


if __name__ == "__main__":
    unittest.main()
