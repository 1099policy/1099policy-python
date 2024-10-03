import unittest
from unittest.mock import patch

from ten99policy.api_resources.abstract.singleton_api_resource import (
    SingletonAPIResource,
)


class TestSingletonAPIResource(unittest.TestCase):

    def setUp(self):
        class ConcreteSingletonResource(SingletonAPIResource):
            OBJECT_NAME = "concrete.singleton"

        self.resource_class = ConcreteSingletonResource

    @patch("ten99policy.api_resources.abstract.api_resource.APIResource.retrieve")
    def test_retrieve(self, mock_super_retrieve):
        # Setup
        mock_super_retrieve.return_value = {"id": "singleton_123"}

        # Execute
        result = self.resource_class.retrieve(param1="value1")

        # Assert
        mock_super_retrieve.assert_called_once_with(None, param1="value1")
        self.assertEqual(result, {"id": "singleton_123"})

    def test_class_url(self):
        # Execute
        url = self.resource_class.class_url()

        # Assert
        self.assertEqual(url, "/api/v1/concrete/singleton")

    def test_instance_url(self):
        # Setup
        instance = self.resource_class()

        # Execute
        url = instance.instance_url()

        # Assert
        self.assertEqual(url, "/api/v1/concrete/singleton")

    def test_class_url_abstract_class(self):
        # Assert
        with self.assertRaises(NotImplementedError):
            SingletonAPIResource.class_url()

    def test_class_url_nested_object_name(self):
        # Setup
        class NestedSingletonResource(SingletonAPIResource):
            OBJECT_NAME = "very.nested.singleton"

        # Execute
        url = NestedSingletonResource.class_url()

        # Assert
        self.assertEqual(url, "/api/v1/very/nested/singleton")

    @patch("ten99policy.api_resources.abstract.api_resource.APIResource.retrieve")
    def test_retrieve_with_api_key(self, mock_super_retrieve):
        # Setup
        mock_super_retrieve.return_value = {"id": "singleton_123"}

        # Execute
        result = self.resource_class.retrieve(api_key="sk_test_123")

        # Assert
        mock_super_retrieve.assert_called_once_with(None, api_key="sk_test_123")
        self.assertEqual(result, {"id": "singleton_123"})

    @patch("ten99policy.api_resources.abstract.api_resource.APIResource.retrieve")
    def test_retrieve_with_ten99policy_version(self, mock_super_retrieve):
        # Setup
        mock_super_retrieve.return_value = {"id": "singleton_123"}

        # Execute
        result = self.resource_class.retrieve(ten99policy_version="2023-03-01")

        # Assert
        mock_super_retrieve.assert_called_once_with(
            None, ten99policy_version="2023-03-01"
        )
        self.assertEqual(result, {"id": "singleton_123"})

    @patch("ten99policy.api_resources.abstract.api_resource.APIResource.retrieve")
    def test_retrieve_with_ten99policy_environment(self, mock_super_retrieve):
        # Setup
        mock_super_retrieve.return_value = {"id": "singleton_123"}

        # Execute
        result = self.resource_class.retrieve(ten99policy_environment="test")

        # Assert
        mock_super_retrieve.assert_called_once_with(
            None, ten99policy_environment="test"
        )
        self.assertEqual(result, {"id": "singleton_123"})


if __name__ == "__main__":
    unittest.main()
