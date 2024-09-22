import unittest
from unittest.mock import patch, MagicMock
from ten99policy.api_requestor import APIRequestor
import ten99policy
import json


class TestAPIRequestor(unittest.TestCase):
    def setUp(self):
        ten99policy.api_key = "sk_test_123"
        self.requestor = APIRequestor()

    @patch("ten99policy.api_requestor.APIRequestor.request_raw")
    def test_request_success(self, mock_request_raw):
        mock_response = MagicMock()
        mock_response.data = json.dumps({"id": "cus_123"})
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_request_raw.return_value = (
            mock_response.data,
            mock_response.status_code,
            mock_response.headers,
            "request_id",
        )

        response, _ = self.requestor.request("get", "/v1/customers")
        self.assertEqual(response.data, {"id": "cus_123"})

    @patch("ten99policy.api_requestor.APIRequestor.request_raw")
    def test_request_error(self, mock_request_raw):
        error_response = {
            "message": "Resource not found",
            "error_code": "resource_missing",
            "type": "invalid_request_error",
            "param": None,
            "code": "404",
        }
        mock_response = MagicMock()
        mock_response.data = json.dumps(error_response)
        mock_response.status_code = 404
        mock_response.headers = {}
        mock_request_raw.return_value = (
            mock_response.data,
            mock_response.status_code,
            mock_response.headers,
            "request_id",
        )

        with self.assertRaises(ten99policy.error.Ten99PolicyError) as context:
            self.requestor.request("get", "/v1/invalid")

        self.assertEqual(str(context.exception), "Resource not found")

    @patch("ten99policy.api_requestor.APIRequestor.request_raw")
    def test_request_with_params(self, mock_request_raw):
        mock_response = MagicMock()
        mock_response.data = json.dumps({"data": [{"id": "cus_123"}]})
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_request_raw.return_value = (
            mock_response.data,
            mock_response.status_code,
            mock_response.headers,
            "request_id",
        )

        response, _ = self.requestor.request(
            "get", "/v1/contractors", params={"limit": 1}
        )
        self.assertEqual(response.data["data"][0]["id"], "cus_123")

    @patch("ten99policy.api_requestor.APIRequestor.request_raw")
    def test_request_with_idempotency_key(self, mock_request_raw):
        mock_response = MagicMock()
        mock_response.data = json.dumps({"id": "cus_123"})
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_request_raw.return_value = (
            mock_response.data,
            mock_response.status_code,
            mock_response.headers,
            "request_id",
        )

        response, _ = self.requestor.request(
            "post", "/v1/contractors", headers={"Idempotency-Key": "unique_key"}
        )
        self.assertEqual(response.data["id"], "cus_123")

    # Add more tests for different HTTP methods, error scenarios, and edge cases
