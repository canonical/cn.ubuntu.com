import unittest
from unittest.mock import patch
from webapp.navigation import get_current_page_bubble


class TestNavigation(unittest.TestCase):
    """Test cases for the navigation.py module"""

    def setUp(self):
        """Set up test data that mirrors the actual
        secondary-navigation.yaml structure"""
        self.mock_navigation_data = {
            "internet-of-things": {
                "title": "物联网",
                "path": "/internet-of-things",
                "children": [
                    {"title": "Overview", "path": "/internet-of-things"},
                    {
                        "title": "Ubuntu Core",
                        "path": "/internet-of-things/core",
                    },
                    {
                        "title": "智能显示屏",
                        "path": "/internet-of-things/smart-displays",
                    },
                ],
            },
            "infrastructure": {
                "title": "基础架构",
                "path": "/infrastructure",
                "children": [
                    {"title": "Overview", "path": "/infrastructure"},
                    {"title": "公有云", "path": "/cloud/public-cloud"},
                    {"title": "OpenStack", "path": "/cloud/openstack"},
                ],
            },
            "desktop": {
                "title": "桌面系统",
                "path": "/desktop",
                "children": [
                    {"title": "Overview", "path": "/desktop"},
                    {"title": "特点", "path": "/desktop/features"},
                ],
            },
            "blog": {
                "title": "博客",
                "path": "/blog",
                "children": [{"title": "Overview", "path": "/blog"}],
            },
            "no-children": {"title": "No Children", "path": "/no-children"},
        }

    def _mock_navigation_lookups(self, navigation_data):
        """Helper method to create lookup dictionaries from navigation data"""
        bubble_path_lookup = {}
        child_path_lookup = {}
        fallback_paths = []

        for key, bubble in navigation_data.items():
            bubble_path = bubble["path"]
            bubble_path_lookup[bubble_path] = bubble

            if "children" in bubble:
                for child in bubble["children"]:
                    child_path = child["path"]
                    child_path_lookup[child_path] = bubble
                    fallback_paths.append(child_path)

            fallback_paths.append(bubble_path)

        # Sort fallback paths by length in descending order (longest first)
        fallback_paths.sort(key=len, reverse=True)

        return bubble_path_lookup, child_path_lookup, fallback_paths

    def _setup_mocks(self, mock_bubble_lookup, mock_child_lookup, 
                     mock_fallback_paths, navigation_data=None):
        """Helper method to set up all mock objects with proper behavior"""
        if navigation_data is None:
            navigation_data = self.mock_navigation_data
            
        bubble_lookup, child_lookup, fallback_paths = (
            self._mock_navigation_lookups(navigation_data)
        )

        mock_bubble_lookup.__contains__ = (
            lambda self, path: path in bubble_lookup
        )
        mock_bubble_lookup.__getitem__ = lambda self, path: bubble_lookup[path]
        mock_child_lookup.__contains__ = (
            lambda self, path: path in child_lookup
        )
        mock_child_lookup.__getitem__ = lambda self, path: child_lookup[path]
        mock_fallback_paths.__iter__ = lambda self: iter(fallback_paths)

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_exact_bubble_match(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test when path exactly matches a navigation bubble's own path"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("/desktop")

        self.assertIsNotNone(result["page_bubble"])
        self.assertEqual(result["page_bubble"]["title"], "桌面系统")
        self.assertEqual(result["page_bubble"]["path"], "/desktop")

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_exact_child_match(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test when path exactly matches a child page within a bubble"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("/desktop/features")

        self.assertIsNotNone(result["page_bubble"])
        self.assertEqual(result["page_bubble"]["title"], "桌面系统")
        self.assertEqual(result["page_bubble"]["path"], "/desktop")
        self.assertTrue(result["page_bubble"]["children"][1]["active"])

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_fallback_match(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test fallback matching for paths that partially match bubble paths"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("/desktop/some-other-page")

        self.assertIsNotNone(result["page_bubble"])
        self.assertEqual(result["page_bubble"]["title"], "桌面系统")

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_no_match(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test when no navigation bubble matches the given path"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("/nonexistent")

        self.assertIsNone(result["page_bubble"])

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_priority_exact_bubble_over_child(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test that exact bubble match takes priority over child match"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("/internet-of-things")

        self.assertIsNotNone(result["page_bubble"])
        self.assertEqual(result["page_bubble"]["title"], "物联网")
        self.assertEqual(result["page_bubble"]["path"], "/internet-of-things")

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_priority_child_over_fallback(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test that child match takes priority over fallback match"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("/cloud/public-cloud")

        self.assertIsNotNone(result["page_bubble"])
        self.assertEqual(result["page_bubble"]["title"], "基础架构")

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_bubble_without_children(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test navigation bubble that has no children"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("/no-children")

        self.assertIsNotNone(result["page_bubble"])
        self.assertEqual(result["page_bubble"]["title"], "No Children")
        self.assertEqual(result["page_bubble"]["path"], "/no-children")

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_empty_path(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test behavior with empty path"""
        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, mock_fallback_paths)

        result = get_current_page_bubble("")

        self.assertIsNone(result["page_bubble"])

    @patch("webapp.navigation._bubble_path_lookup")
    @patch("webapp.navigation._child_path_lookup")
    @patch("webapp.navigation._fallback_paths")
    def test_multiple_fallback_matches(
        self, mock_fallback_paths, mock_child_lookup, mock_bubble_lookup
    ):
        """Test that the longest fallback match is selected"""
        test_data = {
            "short": {
                "title": "Short Path",
                "path": "/parent",
                "children": []
            },
            "long": {
                "title": "Long Path", 
                "path": "/parent/child",
                "children": []
            }
        }

        self._setup_mocks(mock_bubble_lookup, mock_child_lookup, 
                         mock_fallback_paths, test_data)

        result = get_current_page_bubble("/parent/child/grandchild/page")

        self.assertIsNotNone(result["page_bubble"])
        self.assertEqual(result["page_bubble"]["title"], "Long Path")


if __name__ == "__main__":
    unittest.main()
