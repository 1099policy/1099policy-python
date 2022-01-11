from __future__ import absolute_import, division, print_function

import json
from collections import OrderedDict

import pytest

from t99 import six
from t99.t99_response import T99ResponseBase, T99Response


class ResponseTestBase(object):
    @pytest.fixture
    def mock_headers(self):
        return {"idempotency-key": "123456", "request-id": "req_123456"}

    @pytest.fixture
    def mock_response(self, mock_headers):
        code = 200
        headers = mock_headers
        response = T99ResponseBase(code, headers)
        return response

    def test_idempotency_key(self, mock_response, mock_headers):
        assert mock_response.idempotency_key == mock_headers["idempotency-key"]

    def test_request_id(self, mock_response, mock_headers):
        assert mock_response.request_id == mock_headers["request-id"]

    def test_code(self, mock_response, mock_headers):
        assert mock_response.code == 200

    def test_headers(self, mock_response, mock_headers):
        assert mock_response.headers == mock_headers


class TestT99Response(ResponseTestBase):
    def test_body(self, mock_response, mock_body):
        assert mock_response.body == mock_body

    def test_data(self, mock_response, mock_body):
        deserialized = json.loads(mock_body, object_pairs_hook=OrderedDict)
        assert mock_response.data == deserialized

        # Previous assert does not check order, so explicitly check order here
        assert list(six.iterkeys(mock_response.data["metadata"])) == list(
            six.iterkeys(deserialized["metadata"])
        )

    @pytest.fixture
    def mock_response(self, mock_headers, mock_body):
        code = 200
        response = T99Response(mock_body, code, mock_headers)
        return response

    @pytest.fixture
    def mock_body(self):
        return """{
    "id": "ch_12345",
    "object": "charge",
    "amount": 1,
    "metadata": {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5"
    }
}"""
