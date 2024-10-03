import unittest
from unittest.mock import patch, Mock
import json
import datetime
from collections import OrderedDict

from ten99policy.api_requestor import (
    APIRequestor,
    _encode_datetime,
    _encode_nested_dict,
    _api_encode,
    _build_api_url,
)
from ten99policy import error
from ten99policy.http_client import RequestsClient


class TestAPIRequestor(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_key"
        self.api_base = "https://api.test.com"
        self.requestor = APIRequestor(key=self.api_key, api_base=self.api_base)

    def test_init(self):
        self.assertEqual(self.requestor.api_key, self.api_key)
        self.assertEqual(self.requestor.api_base, self.api_base)

    @patch("ten99policy.api_requestor.http_client.RequestsClient")
    def test_init_default_http_client(self, mock_client):
        requestor = APIRequestor()
        self.assertIsInstance(requestor._client, RequestsClient)

    def test_encode_datetime(self):
        dt = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        encoded = _encode_datetime(dt)
        self.assertEqual(encoded, 1672574400)

    def test_encode_nested_dict(self):
        data = {"a": 1, "b": 2}
        encoded = _encode_nested_dict("test", data)
        self.assertEqual(encoded, OrderedDict([("test[a]", 1), ("test[b]", 2)]))

    def test_api_encode(self):
        data = {
            "string": "value",
            "int": 42,
            "list": [1, 2, 3],
            "dict": {"a": 1, "b": 2},
            "datetime": datetime.datetime(
                2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
            ),
        }
        encoded = list(_api_encode(data))
        self.assertIn(("string", "value"), encoded)
        self.assertIn(
            ("int", 42), encoded
        )  # Note: We're now expecting an integer, not a string
        self.assertIn(("list[0]", 1), encoded)
        self.assertIn(("dict[a]", 1), encoded)
        self.assertIn(("datetime", 1672574400), encoded)

    def test_build_api_url(self):
        url = "https://api.test.com/v1/endpoint"
        query = "param1=value1&param2=value2"
        built_url = _build_api_url(url, query)
        self.assertEqual(
            built_url, "https://api.test.com/v1/endpoint?param1=value1&param2=value2"
        )

    @patch("ten99policy.api_requestor.APIRequestor.request_raw")
    def test_request(self, mock_request_raw):
        mock_request_raw.return_value = (
            json.dumps({"result": "success"}),
            200,
            {},
            self.api_key,
        )
        resp, api_key = self.requestor.request("get", "/v1/test")
        self.assertEqual(resp.data, {"result": "success"})
        self.assertEqual(api_key, self.api_key)

    @patch("ten99policy.api_requestor.APIRequestor.request_raw")
    def test_request_stream(self, mock_request_raw):
        mock_stream = Mock()
        mock_request_raw.return_value = (mock_stream, 200, {}, self.api_key)
        resp, api_key = self.requestor.request_stream("get", "/v1/test")
        self.assertEqual(resp.io, mock_stream)
        self.assertEqual(api_key, self.api_key)

    def test_handle_error_response(self):
        with self.assertRaises(error.InvalidRequestError):
            self.requestor.handle_error_response(
                '{"message": "Invalid request", "error_code": "invalid_request"}',
                400,
                {"message": "Invalid request", "error_code": "invalid_request"},
                {},
            )

    def test_request_headers(self):
        headers = self.requestor.request_headers(self.api_key, "post")
        self.assertIn("Authorization", headers)
        self.assertIn("Content-Type", headers)
        self.assertIn("Idempotency-Key", headers)

    @patch("ten99policy.http_client.RequestsClient.request_with_retries")
    def test_request_raw(self, mock_request_with_retries):
        mock_request_with_retries.return_value = (
            json.dumps({"result": "success"}),
            200,
            {},
        )
        requestor = APIRequestor(key=self.api_key, api_base=self.api_base)
        rcontent, rcode, rheaders, api_key = requestor.request_raw("get", "/v1/test")
        self.assertEqual(json.loads(rcontent), {"result": "success"})
        self.assertEqual(rcode, 200)
        self.assertEqual(api_key, self.api_key)
        mock_request_with_retries.assert_called_once()

    def test_interpret_response_success(self):
        resp = self.requestor.interpret_response(
            json.dumps({"result": "success"}), 200, {}
        )
        self.assertEqual(resp.data, {"result": "success"})

    def test_interpret_response_error(self):
        with self.assertRaises(error.APIError):
            self.requestor.interpret_response(json.dumps({"message": "Error"}), 400, {})

    @patch("ten99policy.api_requestor.Ten99PolicyStreamResponse")
    def test_interpret_streaming_response_success(self, mock_stream_response):
        mock_stream = Mock()
        self.requestor.interpret_streaming_response(mock_stream, 200, {})
        mock_stream_response.assert_called_once_with(mock_stream, 200, {})

    def test_interpret_streaming_response_error(self):
        mock_stream = Mock()
        mock_stream.read.return_value = json.dumps({"message": "Error"}).encode()
        with self.assertRaises(error.APIError):
            self.requestor.interpret_streaming_response(mock_stream, 400, {})


if __name__ == "__main__":
    unittest.main()
