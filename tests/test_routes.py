import unittest
from webapp.app import app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        """
        Set up Flask app for testing
        """
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage(self):
        """
        When given the index URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/").status_code, 200)

    def test_not_found(self):
        """
        When given a non-existent URL,
        we should return a 404 status code
        """

        self.assertEqual(self.client.get("/not-found-url").status_code, 404)

    def test_default_cache_control(self):
        """
        Successful responses without their own Cache-Control
        should be cacheable for 1 hour
        """

        response = self.client.get("/fish")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cache_control.max_age, 3600)

    def test_status_endpoints_not_cached(self):
        """
        Status endpoints should never be cached
        """

        response = self.client.get("/_status/check")

        self.assertTrue(response.cache_control.no_store)
        self.assertIsNone(response.cache_control.max_age)


if __name__ == "__main__":
    unittest.main()
