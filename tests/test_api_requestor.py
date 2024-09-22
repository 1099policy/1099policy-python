import unittest
from unittest.mock import patch
from ten99policy.api_requestor import APIRequestor


class TestAPIRequestor(unittest.TestCase):

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_request(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        requestor = APIRequestor()
        response, api_key = requestor.request("get", "/test")
        self.assertEqual(response, {"data": []})
        self.assertEqual(api_key, "api_key")

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_request_with_interpret_response(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        requestor = APIRequestor()
        response, api_key = requestor.request("get", "/test")
        self.assertEqual(response, {"data": []})
        self.assertEqual(api_key, "api_key")

    def test_handle_api_error(self):
        requestor = APIRequestor()
        with self.assertRaises(Exception):
            requestor._handle_api_error({"error": "test_error"})


if __name__ == "__main__":
    unittest.main()
