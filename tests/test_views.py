import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from webapp.app import app
from webapp.views import build_engage_pages_sitemap


class TestBuildEngagePagesSitemap(unittest.TestCase):
    """Tests for webapp.views.build_engage_pages_sitemap"""

    def _make_engage_pages(self, pages):
        engage_pages = MagicMock()
        engage_pages.api.base_url = "https://discourse.ubuntu.com/"
        # get_index returns a 4-tuple:
        # (list of pages, total_count, active_count, current_total)
        engage_pages.get_index.return_value = (pages, 100, 50, len(pages))
        return engage_pages

    def test_builds_links_from_page_list(self):
        pages = [
            {"path": "/engage/foo", "updated": datetime(2026, 1, 2, 3, 4, 5)},
            {"path": "/engage/bar", "updated": datetime(2026, 6, 7, 8, 9, 10)},
        ]
        engage_pages = self._make_engage_pages(pages)
        view = build_engage_pages_sitemap(engage_pages)

        with app.test_request_context("/engage/sitemap.xml"):
            with patch(
                "webapp.views.flask.render_template", return_value=""
            ) as mock_render:
                view()

        _, kwargs = mock_render.call_args
        self.assertEqual(
            kwargs["links"],
            [
                {
                    "url": "https://cn.ubuntu.com/engage/foo",
                    "last_updated": "2026-01-02T03:04:05Z",
                },
                {
                    "url": "https://cn.ubuntu.com/engage/bar",
                    "last_updated": "2026-06-07T08:09:10Z",
                },
            ],
        )

    def test_aborts_404_when_no_pages(self):
        engage_pages = self._make_engage_pages([])
        view = build_engage_pages_sitemap(engage_pages)

        with app.test_request_context("/engage/sitemap.xml"):
            with self.assertRaises(Exception) as ctx:
                view()

        # flask.abort(404) raises an HTTPException with code 404
        self.assertEqual(getattr(ctx.exception, "code", None), 404)


if __name__ == "__main__":
    unittest.main()
