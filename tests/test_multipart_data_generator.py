import unittest
from ten99policy.multipart_data_generator import MultipartDataGenerator
import re


class TestMultipartDataGenerator(unittest.TestCase):
    def test_generate_multipart_data_with_file(self):
        generator = MultipartDataGenerator()
        generator.add_params(
            {
                "purpose": "identity_document",
                "file": ("test.jpg", b"file_content", "image/jpeg"),
            }
        )
        result = generator.get_post_data()

        self.assertIsInstance(result, bytes)
        self.assertIn(b'Content-Disposition: form-data; name="purpose"', result)
        self.assertIn(b"identity_document", result)
        self.assertIn(b'Content-Disposition: form-data; name="file[0]"', result)
        self.assertIn(b"test.jpg", result)
        self.assertIn(b"file_content", result)
        self.assertIn(b"image/jpeg", result)

    def test_generate_multipart_data_with_nested_params(self):
        generator = MultipartDataGenerator()
        generator.add_params({"metadata": {"key1": "value1", "key2": "value2"}})
        result = generator.get_post_data()

        self.assertIsInstance(result, bytes)
        self.assertIn(b'Content-Disposition: form-data; name="metadata[key1]"', result)
        self.assertIn(b"value1", result)
        self.assertIn(b'Content-Disposition: form-data; name="metadata[key2]"', result)
        self.assertIn(b"value2", result)

    # Add more tests for edge cases and different types of data
