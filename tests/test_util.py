# tests/test_util.py
import io
import unittest
from unittest.mock import patch
from ten99policy.util import (
    utf8,
    is_appengine_dev,
    log_debug,
    log_info,
    _test_or_live_environment,
    logfmt,
    secure_compare,
    convert_to_ten99policy_object,
    convert_to_dict,
    populate_headers,
    merge_dicts,
    class_method_variant,
)
import os


# Test with a Ten99PolicyResponse object
class TestUtil(unittest.TestCase):

    def test_utf8(self):
        self.assertEqual(utf8("test"), "test")
        self.assertEqual(utf8("test"), "test")
        self.assertEqual(utf8(b"test"), b"test")

    @patch.dict(os.environ, {"APPENGINE_RUNTIME": "true", "SERVER_SOFTWARE": "Dev"})
    def test_is_appengine_dev(self):
        self.assertTrue(is_appengine_dev())

    @patch.dict(os.environ, {}, clear=True)
    def test_is_not_appengine_dev(self):
        self.assertFalse(is_appengine_dev())

    @patch("ten99policy.util._console_log_level", return_value="debug")
    @patch("ten99policy.util.logger")
    def test_log_debug(self, mock_logger, mock_console_log_level):
        with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
            log_debug("test message", key="value")
            self.assertIn("test message", mock_stderr.getvalue())
        mock_logger.debug.assert_called_once()

    @patch("ten99policy.util._console_log_level", return_value="info")
    @patch("ten99policy.util.logger")
    def test_log_info(self, mock_logger, mock_console_log_level):
        with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
            log_info("test message", key="value")
            self.assertIn("test message", mock_stderr.getvalue())
        mock_logger.info.assert_called_once()

    @patch("ten99policy.api_key", "sk_test_123")
    def test_test_or_live_environment(self):
        self.assertEqual(_test_or_live_environment(), "test")

    def test_logfmt(self):
        props = {"key": "value", "another_key": "another value"}
        formatted = logfmt(props)
        self.assertIn("key=value", formatted)
        self.assertIn("another_key='another value'", formatted)

    def test_secure_compare(self):
        self.assertTrue(secure_compare("test", "test"))
        self.assertFalse(secure_compare("test", "fail"))

    @patch("ten99policy.ten99policy_object.Ten99PolicyObject")
    def test_convert_to_ten99policy_object(self, MockTen99PolicyObject):
        # Set up the mock to return "converted" when construct_from is called
        MockTen99PolicyObject.construct_from.return_value = "converted"

        # Create an instance of the mocked object
        resp = (
            MockTen99PolicyObject.construct_from()
        )  # Call the mock method to get the expected return value

        # Ensure the function is called with the correct parameters
        result = convert_to_ten99policy_object(resp, "api_key")

        self.assertEqual(result, "converted")

    def test_convert_to_dict(self):
        obj = {"key": "value", "nested": {"nested_key": "nested_value"}}
        result = convert_to_dict(obj)
        self.assertEqual(result, obj)

    def test_populate_headers(self):
        self.assertEqual(populate_headers("key"), {"Ten99Policy-Idempotent-Key": "key"})
        self.assertIsNone(populate_headers(None))

    def test_merge_dicts(self):
        x = {"key1": "value1"}
        y = {"key2": "value2"}
        self.assertEqual(merge_dicts(x, y), {"key1": "value1", "key2": "value2"})

    def test_class_method_variant(self):
        class TestClass:
            @class_method_variant("class_method")
            def instance_method(self):
                return "instance_method"

            @classmethod
            def class_method(cls):
                return "class_method"

        instance = TestClass()
        self.assertEqual(instance.instance_method(), "instance_method")
        self.assertEqual(TestClass.instance_method(), "class_method")


if __name__ == "__main__":
    unittest.main()
