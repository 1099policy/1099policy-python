import unittest
from ten99policy.api_resources.abstract.custom_method import custom_method


class TestCustomMethod(unittest.TestCase):
    def test_custom_method_decorator(self):
        class TestResource:
            @custom_method("post", "/test")
            def test_method(cls, id, **params):
                return (id, params)

        result = TestResource.test_method("obj_123", param1="value1")
        self.assertEqual(result, ("obj_123", {"param1": "value1"}))
