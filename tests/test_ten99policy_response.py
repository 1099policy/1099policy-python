import unittest
from ten99policy.ten99policy_response import (
    Ten99PolicyResponse,
    Ten99PolicyStreamResponse,
    Ten99PolicyResponseBase,
)
import json
from collections import OrderedDict


class TestTen99PolicyResponseBase(unittest.TestCase):
    def setUp(self):
        self.code = 200
        self.headers = {
            "Ten99Policy-Idempotent-Key": "idempotency_key_value",
            "request-id": "request_id_value",
        }
        self.response_base = Ten99PolicyResponseBase(self.code, self.headers)

    def test_init(self):
        self.assertEqual(self.response_base.code, self.code)
        self.assertEqual(self.response_base.headers, self.headers)

    def test_idempotency_key(self):
        self.assertEqual(self.response_base.idempotency_key, "idempotency_key_value")

    def test_idempotency_key_missing(self):
        response_base = Ten99PolicyResponseBase(self.code, {})
        self.assertIsNone(response_base.idempotency_key)

    def test_request_id(self):
        self.assertEqual(self.response_base.request_id, "request_id_value")

    def test_request_id_missing(self):
        response_base = Ten99PolicyResponseBase(self.code, {})
        self.assertIsNone(response_base.request_id)


class TestTen99PolicyResponse(unittest.TestCase):
    def setUp(self):
        self.body = json.dumps({"key": "value"})
        self.code = 200
        self.headers = {"Content-Type": "application/json"}
        self.response = Ten99PolicyResponse(self.body, self.code, self.headers)

    def test_init(self):
        self.assertEqual(self.response.body, self.body)
        self.assertEqual(self.response.code, self.code)
        self.assertEqual(self.response.headers, self.headers)
        self.assertEqual(self.response.data, OrderedDict([("key", "value")]))

    def test_data_property(self):
        self.assertEqual(self.response.data, OrderedDict([("key", "value")]))


class TestTen99PolicyStreamResponse(unittest.TestCase):
    def setUp(self):
        self.io = "streaming data"
        self.code = 200
        self.headers = {"Content-Type": "application/octet-stream"}
        self.response = Ten99PolicyStreamResponse(self.io, self.code, self.headers)

    def test_init(self):
        self.assertEqual(self.response.io, self.io)
        self.assertEqual(self.response.code, self.code)
        self.assertEqual(self.response.headers, self.headers)


if __name__ == "__main__":
    unittest.main()
