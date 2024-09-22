import unittest
from ten99policy.ten99policy_object import Ten99PolicyObject


class TestTen99PolicyObject(unittest.TestCase):

    def test_construct_from(self):
        obj = Ten99PolicyObject.construct_from({"key": "value"}, "api_key")
        self.assertEqual(obj.key, "value")
        self.assertEqual(obj.api_key, "api_key")

    def test_to_dict(self):
        obj = Ten99PolicyObject.construct_from({"key": "value"}, "api_key")
        obj_dict = obj.to_dict()
        self.assertEqual(obj_dict, {"key": "value"})


if __name__ == "__main__":
    unittest.main()
