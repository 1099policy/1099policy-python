import unittest
from unittest.mock import patch
from ten99policy.api_resources.list_object import ListObject
from ten99policy.ten99policy_object import (
    Ten99PolicyObject,
)  # Import the correct base class


class TestListObject(unittest.TestCase):

    def setUp(self):
        self.list_object = ListObject.construct_from(
            {
                "url": "https://api.example.com/v1/lists",
                "data": [{"id": "item_1"}, {"id": "item_2"}],
                "has_more": True,
            },
            "list_object_key",  # Add the required key argument here
        )

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_list(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        result = self.list_object.list()
        self.assertIsInstance(
            result, Ten99PolicyObject
        )  # Updated to check for Ten99PolicyObject

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_create(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        result = self.list_object.create()
        self.assertIsInstance(
            result, Ten99PolicyObject
        )  # Updated to check for Ten99PolicyObject

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_retrieve(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        result = self.list_object.retrieve("item_1")
        self.assertIsInstance(
            result, Ten99PolicyObject
        )  # Updated to check for Ten99PolicyObject

    def test_getitem(self):
        self.assertEqual(self.list_object["url"], "https://api.example.com/v1/lists")
        with self.assertRaises(KeyError):
            _ = self.list_object[0]

    def test_iter(self):
        data = list(iter(self.list_object))
        self.assertEqual(len(data), 2)

    def test_len(self):
        self.assertEqual(len(self.list_object), 2)

    def test_reversed(self):
        data = list(reversed(self.list_object))
        self.assertEqual(data[0]["id"], "item_2")

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_auto_paging_iter(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        iterator = self.list_object.auto_paging_iter()
        self.assertIsInstance(next(iterator), dict)

    def test_empty_list(self):
        empty_list = ListObject.empty_list()
        self.assertEqual(len(empty_list.data), 0)

    def test_is_empty(self):
        self.assertFalse(self.list_object.is_empty)
        empty_list = ListObject.empty_list()
        self.assertTrue(empty_list.is_empty)

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_next_page(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        next_page = self.list_object.next_page()
        self.assertIsInstance(
            next_page, Ten99PolicyObject
        )  # Updated to check for Ten99PolicyObject

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_previous_page(self, mock_request):
        mock_request.return_value = ({"data": []}, "api_key")
        previous_page = self.list_object.previous_page()
        self.assertIsInstance(
            previous_page, Ten99PolicyObject
        )  # Updated to check for Ten99PolicyObject


if __name__ == "__main__":
    unittest.main()
