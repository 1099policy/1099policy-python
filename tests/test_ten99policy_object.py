import unittest
from unittest.mock import patch, Mock
import datetime
import json

from ten99policy.ten99policy_object import Ten99PolicyObject
from ten99policy import util, api_requestor


class TestTen99PolicyObject(unittest.TestCase):

    def setUp(self):
        self.obj = Ten99PolicyObject(
            id="obj_123",
            api_key="sk_test_123",
            ten99policy_version="2023-03-01",
            ten99policy_environment="test",
        )

    def test_init(self):
        self.assertEqual(self.obj.id, "obj_123")
        self.assertEqual(self.obj.api_key, "sk_test_123")
        self.assertEqual(self.obj.ten99policy_version, "2023-03-01")
        self.assertEqual(self.obj.ten99policy_environment, "test")

    def test_update(self):
        self.obj.update({"foo": "bar"})
        self.assertEqual(self.obj["foo"], "bar")
        self.assertIn("foo", self.obj._unsaved_values)

    def test_setattr(self):
        self.obj.new_attr = "value"
        self.assertEqual(self.obj["new_attr"], "value")
        self.assertIn("new_attr", self.obj._unsaved_values)

    def test_getattr(self):
        self.obj["get_attr"] = "test"
        self.assertEqual(self.obj.get_attr, "test")

        with self.assertRaises(AttributeError):
            self.obj.nonexistent_attr

    def test_delattr(self):
        self.obj["del_attr"] = "test"
        del self.obj.del_attr
        self.assertNotIn("del_attr", self.obj)

    def test_setitem_empty_string(self):
        with self.assertRaises(ValueError):
            self.obj["empty"] = ""

    def test_getitem_transient(self):
        self.obj._transient_values.add("transient")
        with self.assertRaises(KeyError):
            self.obj["transient"]

    def test_serialize(self):
        self.obj["serialize_me"] = "value"
        serialized = self.obj.serialize({})
        self.assertEqual(serialized["serialize_me"], "value")

    @patch("ten99policy.util.convert_to_ten99policy_object")
    def test_refresh_from(self, mock_convert):
        mock_convert.return_value = "converted"
        self.obj.refresh_from({"new_key": "new_value"})
        self.assertEqual(self.obj["new_key"], "converted")

    @patch("ten99policy.api_requestor.APIRequestor")
    def test_request(self, mock_requestor):
        mock_instance = Mock()
        mock_requestor.return_value = mock_instance
        mock_instance.request.return_value = ({"id": "resp_123"}, "sk_test_123")

        response = self.obj.request("get", "/v1/endpoint")

        mock_requestor.assert_called_once_with(
            key="sk_test_123",
            api_base=None,
            api_version="2023-03-01",
            environment="test",
        )
        # Update the expected params to be an empty dict instead of None
        mock_instance.request.assert_called_once_with("get", "/v1/endpoint", {}, None)
        self.assertIsNotNone(response)

    def test_to_dict_recursive(self):
        nested_obj = Ten99PolicyObject(id="nested_123")
        self.obj["nested"] = nested_obj
        self.obj["list"] = [1, nested_obj]

        result = self.obj.to_dict_recursive()

        self.assertIsInstance(result["nested"], dict)
        self.assertEqual(result["nested"]["id"], "nested_123")
        self.assertIsInstance(result["list"][1], dict)

    def test_repr_json_encoder(self):
        encoder = Ten99PolicyObject.ReprJSONEncoder()
        # Use UTC time to avoid time zone issues
        dt = datetime.datetime(2023, 3, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        encoded = encoder.encode({"date": dt})

        # Parse the encoded JSON
        decoded = json.loads(encoded)

        # Check if the 'date' key exists and its value is a number (timestamp)
        self.assertIn("date", decoded)
        self.assertTrue(isinstance(decoded["date"], (int, float)))

        # Convert the timestamp back to a datetime object (assuming UTC)
        encoded_dt = datetime.datetime.fromtimestamp(
            decoded["date"], tz=datetime.timezone.utc
        )

        # Check if the encoded datetime is exactly the same as the original
        self.assertEqual(encoded_dt, dt)

    def test_construct_from(self):
        values = {"id": "const_123", "key": "value"}
        obj = Ten99PolicyObject.construct_from(values, "sk_test_123")
        self.assertEqual(obj.id, "const_123")
        self.assertEqual(obj["key"], "value")

    def test_pickling(self):
        import pickle

        pickled = pickle.dumps(self.obj)
        unpickled = pickle.loads(pickled)
        self.assertEqual(self.obj.id, unpickled.id)
        self.assertEqual(self.obj.api_key, unpickled.api_key)

    def test_serialize_empty_string(self):
        self.obj["empty"] = None
        serialized = self.obj.serialize({})
        self.assertEqual(serialized["empty"], "")

    def test_dirty_json_parse(self):
        values = {"key": "{'nested': 'value'}"}
        obj = Ten99PolicyObject.construct_from(values, "sk_test_123")
        self.assertEqual(obj["key"], {"nested": "value"})

    def test_copy(self):
        self.obj["copy_me"] = "value"
        copied = self.obj.__copy__()
        self.assertEqual(copied["copy_me"], "value")
        self.assertIsNot(copied, self.obj)

    def test_deepcopy(self):
        nested = {"nested": "value"}
        self.obj["deep_copy"] = nested
        deep_copied = self.obj.__deepcopy__({})
        self.assertEqual(deep_copied["deep_copy"], nested)
        self.assertIsNot(deep_copied["deep_copy"], nested)


if __name__ == "__main__":
    unittest.main()
