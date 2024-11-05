import unittest
from unittest import mock
from ten99policy.api_resources.abstract.custom_method import custom_method
from ten99policy.util import class_method_variant


class MockResource:
    @classmethod
    def class_url(cls):
        return "/mock_resources"

    @classmethod
    def _static_request(cls, http_verb, url, **params):
        pass

    @classmethod
    def _static_request_stream(cls, http_verb, url, **params):
        pass

    # Mock instance method to test method prefixing
    def existing_method(self):
        pass


class TestCustomMethod(unittest.TestCase):
    def setUp(self):
        self.MockResource = MockResource

    def test_custom_method_adds_class_method(self):
        """Test that custom_method adds a class method when it doesn't exist."""

        @custom_method("new_method", "get")
        class Resource(self.MockResource):
            pass

        self.assertTrue(hasattr(Resource, "new_method"))
        # Inspect the class's __dict__ to check if it's a classmethod
        self.assertTrue(isinstance(Resource.__dict__["new_method"], classmethod))

    def test_custom_method_invalid_http_verb(self):
        """Test that custom_method raises ValueError for invalid HTTP verbs."""
        with self.assertRaises(ValueError) as context:

            @custom_method("invalid_method", "patch")
            class Resource(self.MockResource):
                pass

        self.assertIn("Invalid http_verb: patch", str(context.exception))

    def test_custom_method_with_http_path_none(self):
        """Test that custom_method uses the method name as http_path when http_path is None."""

        @custom_method("retrieve", "get")
        class Resource(self.MockResource):
            pass

        self.assertTrue(hasattr(Resource, "retrieve"))
        self.assertTrue(isinstance(Resource.__dict__["retrieve"], classmethod))

        with mock.patch.object(Resource, "_static_request") as mock_request:
            # Invoke the class method correctly without passing the class
            response = Resource.retrieve("sid123", param="value")
            expected_url = "/mock_resources/sid123/retrieve"
            mock_request.assert_called_with("get", expected_url, param="value")

    def test_custom_method_with_custom_http_path(self):
        """Test that custom_method uses the provided http_path."""

        @custom_method("custom_retrieve", "get", http_path="custom_path")
        class Resource(self.MockResource):
            pass

        self.assertTrue(hasattr(Resource, "custom_retrieve"))
        self.assertTrue(isinstance(Resource.__dict__["custom_retrieve"], classmethod))

        with mock.patch.object(Resource, "_static_request") as mock_request:
            # Invoke the class method correctly without passing the class
            response = Resource.custom_retrieve("sid123", param="value")
            expected_url = "/mock_resources/sid123/custom_path"
            mock_request.assert_called_with("get", expected_url, param="value")

    def test_custom_method_is_streaming_true(self):
        """Test that custom_method creates a streaming class method when is_streaming is True."""

        @custom_method("stream_method", "post", is_streaming=True)
        class Resource(self.MockResource):
            pass

        self.assertTrue(hasattr(Resource, "stream_method"))
        self.assertTrue(isinstance(Resource.__dict__["stream_method"], classmethod))

        with mock.patch.object(
            Resource, "_static_request_stream"
        ) as mock_request_stream:
            # Invoke the streaming class method correctly without passing the class
            response = Resource.stream_method("sid123", param="value")
            expected_url = "/mock_resources/sid123/stream_method"
            mock_request_stream.assert_called_with("post", expected_url, param="value")

    def test_custom_method_overrides_existing_method(self):
        """Test that custom_method prefixes existing methods and creates class method."""

        @custom_method("existing_method", "delete")
        class Resource(self.MockResource):
            pass

        # Check that the new class method is prefixed with '_cls_'
        self.assertTrue(hasattr(Resource, "_cls_existing_method"))
        self.assertTrue(
            isinstance(Resource.__dict__["_cls_existing_method"], classmethod)
        )

        # Verify that the new class method is a classmethod
        new_class_method = Resource.__dict__["_cls_existing_method"]
        self.assertTrue(isinstance(new_class_method, classmethod))

        with mock.patch.object(Resource, "_static_request") as mock_request:
            # Invoke the new class method correctly without passing the class
            response = Resource._cls_existing_method("sid123", param="value")
            expected_url = "/mock_resources/sid123/existing_method"
            mock_request.assert_called_with("delete", expected_url, param="value")

        # Verify that the original instance method still exists
        instance = Resource()
        self.assertTrue(hasattr(instance, "existing_method"))

        # Assuming util.class_method_variant correctly decorates the instance method
        # We can test if it's been called by checking if the instance method is callable
        self.assertTrue(callable(instance.existing_method))

    def test_custom_method_preserves_existing_instance_method_behavior(self):
        """Test that the original instance method behavior is preserved after decoration."""

        @custom_method("existing_method", "put")
        class Resource(self.MockResource):
            def existing_method(self):
                return "original behavior"

        instance = Resource()
        self.assertTrue(hasattr(instance, "existing_method"))

        with mock.patch.object(Resource, "_static_request") as mock_request:
            mock_request.return_value = "class method response"
            # Invoke the class method correctly without passing the class
            response = Resource.existing_method("sid123", param="value")
            expected_url = "/mock_resources/sid123/existing_method"
            mock_request.assert_called_with("put", expected_url, param="value")
            self.assertEqual(response, "class method response")

    def test_custom_method_with_existing_non_method_attribute(self):
        """Test that custom_method handles cases where the existing attribute is not a method."""

        @custom_method("attribute_name", "get")
        class Resource(self.MockResource):
            attribute_name = "not a method"

        # It should still prefix the new class method and replace the attribute with a method variant
        self.assertTrue(hasattr(Resource, "_cls_attribute_name"))
        self.assertTrue(
            isinstance(Resource.__dict__["_cls_attribute_name"], classmethod)
        )
        self.assertTrue(hasattr(Resource, "attribute_name"))

        method = getattr(Resource, "_cls_attribute_name")
        self.assertTrue(
            isinstance(Resource.__dict__["_cls_attribute_name"], classmethod)
        )

        with mock.patch.object(Resource, "_static_request") as mock_request:
            # Invoke the class method correctly without passing the class
            response = Resource._cls_attribute_name("sid123")
            expected_url = "/mock_resources/sid123/attribute_name"
            mock_request.assert_called_with("get", expected_url)

    def test_custom_method_multiple_methods(self):
        """Test that multiple custom methods can be added to a class."""

        @custom_method("method_one", "get")
        @custom_method("method_two", "post")
        class Resource(self.MockResource):
            pass

        self.assertTrue(hasattr(Resource, "method_one"))
        self.assertTrue(isinstance(Resource.__dict__["method_one"], classmethod))
        self.assertTrue(hasattr(Resource, "method_two"))
        self.assertTrue(isinstance(Resource.__dict__["method_two"], classmethod))

        with mock.patch.object(Resource, "_static_request") as mock_request:
            # Invoke method_one correctly without passing the class
            Resource.method_one("sid123")
            expected_url_one = "/mock_resources/sid123/method_one"
            mock_request.assert_any_call("get", expected_url_one)

            # Invoke method_two correctly without passing the class
            Resource.method_two("sid123", data="value")
            expected_url_two = "/mock_resources/sid123/method_two"
            mock_request.assert_any_call("post", expected_url_two, data="value")

    def test_class_method_variant_decorator(self):
        """Test that class_method_variant decorator is applied correctly."""
        with mock.patch(
            "ten99policy.util.class_method_variant", wraps=class_method_variant
        ) as mock_variant:

            @custom_method("test_variant", "get")
            class Resource(self.MockResource):
                def test_variant(self, sid, param):
                    return "instance method response"

            # Ensure class_method_variant was called
            mock_variant.assert_called_once()

            # Check that the class method was added
            self.assertTrue(hasattr(Resource, "test_variant"))
            self.assertTrue(hasattr(Resource, "_cls_test_variant"))
            self.assertTrue(
                isinstance(Resource.__dict__["_cls_test_variant"], classmethod)
            )

            # Mock the _static_request to return a value
            with mock.patch.object(Resource, "_static_request") as mock_request:
                mock_request.return_value = "class method response"
                response = Resource.test_variant("sid999", param="value")
                expected_url = "/mock_resources/sid999/test_variant"
                mock_request.assert_called_with("get", expected_url, param="value")
                self.assertEqual(response, "class method response")


if __name__ == "__main__":
    unittest.main()
