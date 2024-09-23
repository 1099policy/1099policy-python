import unittest
from unittest.mock import patch
from ten99policy.api_resources.abstract.updateable_api_resource import (
    UpdateableAPIResource,
)
from ten99policy import util, error


class TestUpdateableAPIResource(unittest.TestCase):

    def setUp(self):
        class ConcreteUpdateableAPIResource(UpdateableAPIResource):
            OBJECT_NAME = "updateable_api_resource"

        self.resource_class = ConcreteUpdateableAPIResource
        self.resource = self.resource_class()
        self.resource.id = "test_id"

    @patch(
        "ten99policy.api_resources.abstract.updateable_api_resource.APIResource._static_request"
    )
    def test_modify(self, mock_static_request):
        mock_static_request.return_value = {"id": "test_id", "updated": True}

        result = self.resource_class.modify("test_id", updated=True)

        self.assertEqual(result, {"id": "test_id", "updated": True})
        mock_static_request.assert_called_once_with(
            "put", "/api/v1/updateable_api_resource/test_id", updated=True
        )

    @patch("ten99policy.api_resources.abstract.updateable_api_resource.quote_plus")
    def test_modify_with_special_chars(self, mock_quote_plus):
        mock_quote_plus.return_value = "test%2Bid"
        with patch.object(
            self.resource_class, "_static_request"
        ) as mock_static_request:
            mock_static_request.return_value = {"id": "test+id", "updated": True}

            result = self.resource_class.modify("test+id", updated=True)

            self.assertEqual(result, {"id": "test+id", "updated": True})
            mock_static_request.assert_called_once_with(
                "put", "/api/v1/updateable_api_resource/test%2Bid", updated=True
            )

    @patch(
        "ten99policy.api_resources.abstract.updateable_api_resource.APIResource.request"
    )
    def test_save_with_updates(self, mock_request):
        mock_request.return_value = {"id": "test_id", "updated": True}
        self.resource.updated = True

        result = self.resource.save()

        self.assertEqual(result, self.resource)
        self.assertTrue(self.resource.updated)
        mock_request.assert_called_once_with(
            "put", "/api/v1/updateable_api_resource/test_id", {"updated": True}, None
        )

    @patch(
        "ten99policy.api_resources.abstract.updateable_api_resource.APIResource.request"
    )
    def test_save_without_updates(self, mock_request):
        result = self.resource.save()

        self.assertEqual(result, self.resource)
        mock_request.assert_not_called()

    @patch(
        "ten99policy.api_resources.abstract.updateable_api_resource.APIResource.request"
    )
    @patch("ten99policy.util.log_debug")
    def test_save_already_saved(self, mock_log_debug, mock_request):
        self.resource._previous = {"id": "test_id", "updated": True}
        self.resource.updated = True
        result = self.resource.save()

        self.assertEqual(result, self.resource)
        mock_request.assert_called_once_with(
            "put",
            "/api/v1/updateable_api_resource/test_id",
            {"updated": True},  # The 'updated' parameter is still being sent
            None,
        )
        mock_log_debug.assert_not_called()  # Changed this line

    @patch(
        "ten99policy.api_resources.abstract.updateable_api_resource.APIResource.request"
    )
    @patch("ten99policy.util.populate_headers")
    def test_save_with_idempotency_key(self, mock_populate_headers, mock_request):
        mock_populate_headers.return_value = {"Idempotency-Key": "test_key"}
        mock_request.return_value = {"id": "test_id", "updated": True}
        self.resource.updated = True

        result = self.resource.save(idempotency_key="test_key")

        self.assertEqual(result, self.resource)
        self.assertTrue(self.resource.updated)
        mock_request.assert_called_once_with(
            "put",
            "/api/v1/updateable_api_resource/test_id",
            {"updated": True},
            {"Idempotency-Key": "test_key"},
        )

    def test_instance_url(self):
        self.assertEqual(
            self.resource.instance_url(), "/api/v1/updateable_api_resource/test_id"
        )

    def test_instance_url_without_id(self):
        self.resource.id = None
        with self.assertRaises(error.InvalidRequestError):
            self.resource.instance_url()


if __name__ == "__main__":
    unittest.main()
