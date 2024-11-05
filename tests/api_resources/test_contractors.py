import unittest
from unittest.mock import patch, MagicMock
import ten99policy
from ten99policy import Contractors


class TestContractors(unittest.TestCase):

    def setUp(self):
        ten99policy.api_key = "sk_test_123"

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_list_contractors(self, mock_request):
        mock_response = MagicMock()
        mock_response.data = [{"id": "cus_123", "email": "test@example.com"}]
        mock_request.return_value = (mock_response, "api_key")

        contractors = Contractors.list()

        self.assertEqual(len(contractors.data), 1)
        self.assertEqual(contractors.data[0]["id"], "cus_123")
        self.assertEqual(contractors.data[0]["email"], "test@example.com")

    @patch("ten99policy.api_requestor.APIRequestor.request")
    def test_retrieve_contractor(self, mock_request):
        mock_response = {"id": "cus_123", "email": "test@example.com"}
        mock_request.return_value = (mock_response, "api_key")

        contractor = Contractors.retrieve("cus_123")

        self.assertEqual(contractor["id"], "cus_123")
        self.assertEqual(contractor["email"], "test@example.com")
