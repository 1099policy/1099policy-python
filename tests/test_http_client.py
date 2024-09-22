import json
import unittest
from unittest.mock import patch, MagicMock, Mock
from ten99policy.http_client import HTTPClient


class ConcreteHTTPClient(HTTPClient):
    def request(self, method, url, headers, post_data=None):
        # Implement a basic request method for testing
        return 200, '{"success": true}', {}


class TestHTTPClient(unittest.TestCase):
    def setUp(self):
        self.client = ConcreteHTTPClient()

    def test_request_get(self):
        status, content, _ = self.client.request(
            "get", "https://api.ten99policy.com/v1/test", headers={}
        )
        self.assertEqual(status, 200)
        self.assertEqual(content, '{"success": true}')

    def test_request_post(self):
        client = ConcreteHTTPClient()

        # Perform the request
        status, content, headers = client.request(
            "post",
            "https://api.example.com/endpoint",
            headers={"Content-Type": "application/json"},
            post_data={"key": "value"},
        )

        # Assert the response
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(content), {"success": True})
        self.assertEqual(
            headers, {}
        )  # Assuming ConcreteHTTPClient returns an empty dict for headers
