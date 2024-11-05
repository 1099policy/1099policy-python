import unittest
from unittest.mock import patch
from ten99policy.api_resources.abstract.nested_resource_class_methods import (
    nested_resource_class_methods,
)


class TestNestedResourceClassMethods(unittest.TestCase):

    def setUp(self):
        # Create a mock class to apply the decorator
        class MockResource:
            @classmethod
            def class_url(cls):
                return "https://api.example.com/resources"

        self.MockResource = MockResource

    @patch("ten99policy.api_requestor.APIRequestor")
    @patch("ten99policy.util.convert_to_ten99policy_object")
    def test_nested_resource_class_methods_create(
        self, mock_convert, mock_api_requestor
    ):
        mock_api_requestor.return_value.request.return_value = ("response", "api_key")
        mock_convert.return_value = "converted"

        @nested_resource_class_methods("resource", operations=["create"])
        class ResourceWithCreate(self.MockResource):
            pass

        # Test the create method
        result = ResourceWithCreate.create_resource("123", param1="value1")
        self.assertEqual(result, "converted")
        mock_api_requestor.return_value.request.assert_called_once()
        self.assertIn("post", mock_api_requestor.return_value.request.call_args[0])

    @patch("ten99policy.api_requestor.APIRequestor")
    @patch("ten99policy.util.convert_to_ten99policy_object")
    def test_nested_resource_class_methods_retrieve(
        self, mock_convert, mock_api_requestor
    ):
        mock_api_requestor.return_value.request.return_value = ("response", "api_key")
        mock_convert.return_value = "converted"

        @nested_resource_class_methods("resource", operations=["retrieve"])
        class ResourceWithRetrieve(self.MockResource):
            pass

        # Test the retrieve method
        result = ResourceWithRetrieve.retrieve_resource("123", "456")
        self.assertEqual(result, "converted")
        mock_api_requestor.return_value.request.assert_called_once()
        self.assertIn("get", mock_api_requestor.return_value.request.call_args[0])

    @patch("ten99policy.api_requestor.APIRequestor")
    @patch("ten99policy.util.convert_to_ten99policy_object")
    def test_nested_resource_class_methods_update(
        self, mock_convert, mock_api_requestor
    ):
        mock_api_requestor.return_value.request.return_value = ("response", "api_key")
        mock_convert.return_value = "converted"

        @nested_resource_class_methods("resource", operations=["update"])
        class ResourceWithUpdate(self.MockResource):
            pass

        # Test the update method
        result = ResourceWithUpdate.modify_resource("123", "456", param1="value1")
        self.assertEqual(result, "converted")
        mock_api_requestor.return_value.request.assert_called_once()
        self.assertIn("post", mock_api_requestor.return_value.request.call_args[0])

    @patch("ten99policy.api_requestor.APIRequestor")
    @patch("ten99policy.util.convert_to_ten99policy_object")
    def test_nested_resource_class_methods_delete(
        self, mock_convert, mock_api_requestor
    ):
        mock_api_requestor.return_value.request.return_value = ("response", "api_key")
        mock_convert.return_value = "converted"

        @nested_resource_class_methods("resource", operations=["delete"])
        class ResourceWithDelete(self.MockResource):
            pass

        # Test the delete method
        result = ResourceWithDelete.delete_resource("123", "456")
        self.assertEqual(result, "converted")
        mock_api_requestor.return_value.request.assert_called_once()
        self.assertIn("delete", mock_api_requestor.return_value.request.call_args[0])

    @patch("ten99policy.api_requestor.APIRequestor")
    @patch("ten99policy.util.convert_to_ten99policy_object")
    def test_nested_resource_class_methods_list(self, mock_convert, mock_api_requestor):
        mock_api_requestor.return_value.request.return_value = ("response", "api_key")
        mock_convert.return_value = "converted"

        @nested_resource_class_methods("resource", operations=["list"])
        class ResourceWithList(self.MockResource):
            pass

        # Test the list method
        result = ResourceWithList.list_resources("123")
        self.assertEqual(result, "converted")
        mock_api_requestor.return_value.request.assert_called_once()
        self.assertIn("get", mock_api_requestor.return_value.request.call_args[0])

    def test_nested_resource_class_methods_invalid_operation(self):
        with self.assertRaises(ValueError) as context:

            @nested_resource_class_methods("resource", operations=["invalid_operation"])
            class InvalidResource(self.MockResource):
                pass

        self.assertEqual(str(context.exception), "Unknown operation: invalid_operation")


if __name__ == "__main__":
    unittest.main()
