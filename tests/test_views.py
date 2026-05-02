import unittest
from unittest.mock import MagicMock, patch

from webapp.app import app
from webapp.views import build_engage_index


def _make_engage_docs(current_total=29):
    """Build a mock engage_docs object with a configurable get_index."""
    engage_docs = MagicMock()
    engage_docs.api.base_url = "https://discourse.ubuntu.com/"
    engage_docs.get_index.return_value = (
        [{"topic_name": "Item"}],
        100,
        50,
        current_total,
    )
    return engage_docs


class TestBuildEngageIndex(unittest.TestCase):
    """Tests for webapp.views.build_engage_index pagination behavior"""

    def test_default_page_uses_offset_zero(self):
        engage_docs = _make_engage_docs()
        view = build_engage_index(engage_docs)

        with app.test_request_context("/engage"):
            with patch("webapp.views.flask.render_template", return_value=""):
                view()

        engage_docs.get_index.assert_called_once_with(
            14, 0, key="is_static", value=None
        )

    def test_explicit_page_calculates_offset(self):
        engage_docs = _make_engage_docs()
        view = build_engage_index(engage_docs)

        with app.test_request_context("/engage?page=3"):
            with patch("webapp.views.flask.render_template", return_value=""):
                view()

        # page 3 with posts_per_page 14 → offset 28
        engage_docs.get_index.assert_called_once_with(
            14, 28, key="is_static", value=None
        )

    def test_total_pages_rounds_up(self):
        engage_docs = _make_engage_docs(current_total=29)
        view = build_engage_index(engage_docs)

        with app.test_request_context("/engage"):
            with patch(
                "webapp.views.flask.render_template", return_value=""
            ) as mock_render:
                view()

        _, kwargs = mock_render.call_args
        # ceil(29 / 14) == 3
        self.assertEqual(kwargs["total_pages"], 3)
        self.assertEqual(kwargs["posts_per_page"], 14)

    def test_total_pages_exact_division(self):
        engage_docs = _make_engage_docs(current_total=28)
        view = build_engage_index(engage_docs)

        with app.test_request_context("/engage"):
            with patch(
                "webapp.views.flask.render_template", return_value=""
            ) as mock_render:
                view()

        _, kwargs = mock_render.call_args
        # ceil(28 / 14) == 2
        self.assertEqual(kwargs["total_pages"], 2)

    def test_passes_metadata_and_query_args_to_template(self):
        engage_docs = _make_engage_docs()
        view = build_engage_index(engage_docs)

        with app.test_request_context(
            "/engage?page=2&topic=cloud&sort=newest"
        ):
            with patch(
                "webapp.views.flask.render_template", return_value=""
            ) as mock_render:
                view()

        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], "engage/index.html")
        self.assertEqual(kwargs["metadata"], [{"topic_name": "Item"}])
        self.assertEqual(kwargs["page"], 2)
        self.assertEqual(kwargs["topic"], "cloud")
        self.assertEqual(kwargs["sort"], "newest")
        self.assertEqual(kwargs["forum_url"], "https://discourse.ubuntu.com/")


if __name__ == "__main__":
    unittest.main()
