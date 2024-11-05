import unittest
from unittest.mock import patch

from ten99policy.api_resources.abstract.deletable_api_resource import (
    DeletableAPIResource,
)


class TestDeletableAPIResource(unittest.TestCase):

    def setUp(self):
        class ConcreteDeletableResource(DeletableAPIResource):
            OBJECT_NAME = "deletable"

        self.resource_class = ConcreteDeletableResource
        self.resource = self.resource_class.construct_from(
            {"id": "res_123", "foo": "bar"}, "fake_api_key"
        )

    @patch(
        "ten99policy.api_resources.abstract.api_resource.APIResource._static_request"
    )
    def test_cls_delete(self, mock_static_request):
        # Setup
        mock_static_request.return_value = {"id": "res_123", "deleted": True}

        # Execute
        result = self.resource_class._cls_delete("res_123", param1="value1")

        # Assert
        mock_static_request.assert_called_once_with(
            "delete", "/api/v1/deletable/res_123", param1="value1"
        )
        self.assertEqual(result, {"id": "res_123", "deleted": True})

    @patch("ten99policy.api_resources.abstract.api_resource.APIResource.request")
    def test_delete_instance_method(self, mock_request):
        # Setup
        mock_request.return_value = {"id": "res_123", "deleted": True}

        # Execute
        result = self.resource.delete(param1="value1")

        # Assert
        mock_request.assert_called_once_with(
            "delete", "/api/v1/deletable/res_123", {"param1": "value1"}
        )
        self.assertEqual(result, self.resource)
        self.assertEqual(self.resource.deleted, True)

    @patch(
        "ten99policy.api_resources.abstract.api_resource.APIResource._static_request"
    )
    def test_cls_delete_with_special_chars(self, mock_static_request):
        # Setup
        mock_static_request.return_value = {"id": "res+123", "deleted": True}

        # Execute
        result = self.resource_class._cls_delete("res+123")

        # Assert
        mock_static_request.assert_called_once_with(
            "delete", "/api/v1/deletable/res%2B123"
        )
        self.assertEqual(result, {"id": "res+123", "deleted": True})

    @patch(
        "ten99policy.api_resources.abstract.api_resource.APIResource._static_request"
    )
    def test_cls_delete_with_api_key(self, mock_static_request):
        # Setup
        mock_static_request.return_value = {"id": "res_123", "deleted": True}

        # Execute
        result = self.resource_class._cls_delete("res_123", api_key="sk_test_1234")

        # Assert
        mock_static_request.assert_called_once_with(
            "delete", "/api/v1/deletable/res_123", api_key="sk_test_1234"
        )
        self.assertEqual(result, {"id": "res_123", "deleted": True})

    @patch("ten99policy.api_resources.abstract.api_resource.APIResource.request")
    def test_delete_instance_method_with_ten99policy_version(self, mock_request):
        # Setup
        mock_request.return_value = {"id": "res_123", "deleted": True}

        # Execute
        result = self.resource.delete(ten99policy_version="2023-03-01")

        # Assert
        mock_request.assert_called_once_with(
            "delete", "/api/v1/deletable/res_123", {"ten99policy_version": "2023-03-01"}
        )
        self.assertEqual(result, self.resource)
        self.assertEqual(self.resource.deleted, True)

    @patch("ten99policy.api_resources.abstract.api_resource.APIResource.request")
    def test_delete_instance_method_with_ten99policy_environment(self, mock_request):
        # Setup
        mock_request.return_value = {"id": "res_123", "deleted": True}

        # Execute
        result = self.resource.delete(ten99policy_environment="test")

        # Assert
        mock_request.assert_called_once_with(
            "delete", "/api/v1/deletable/res_123", {"ten99policy_environment": "test"}
        )
        self.assertEqual(result, self.resource)
        self.assertEqual(self.resource.deleted, True)


if __name__ == "__main__":
    unittest.main()
