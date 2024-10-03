# tests/test_multipart_data_generator.py
import unittest
import io
from ten99policy.multipart_data_generator import MultipartDataGenerator


class TestMultipartDataGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = MultipartDataGenerator()

    def test_add_params_with_string(self):
        # Test adding params with string values
        params = {"key1": "value1", "key2": "value2"}
        self.generator.add_params(params)
        post_data = self.generator.get_post_data().decode("utf-8")

        # Check if the params are correctly added
        self.assertIn('Content-Disposition: form-data; name="key1"', post_data)
        self.assertIn('Content-Disposition: form-data; name="key2"', post_data)
        self.assertIn("value1", post_data)
        self.assertIn("value2", post_data)

    def test_add_params_with_none_value(self):
        # Test adding params with None value
        params = {"key1": "value1", "key2": None}
        self.generator.add_params(params)
        post_data = self.generator.get_post_data().decode("utf-8")

        # Check if the None value is skipped
        self.assertIn('Content-Disposition: form-data; name="key1"', post_data)
        self.assertIn("value1", post_data)
        self.assertNotIn('Content-Disposition: form-data; name="key2"', post_data)

    def test_add_params_with_int_value(self):
        # Test adding params with integer value
        params = {"key1": 123}
        self.generator.add_params(params)
        post_data = self.generator.get_post_data().decode("utf-8")

        # Check if the integer value is correctly added
        self.assertIn('Content-Disposition: form-data; name="key1"', post_data)
        self.assertIn("123", post_data)

    def test_add_params_with_unicode(self):
        # Test adding params with unicode value
        params = {"key1": "值"}
        self.generator.add_params(params)
        post_data = self.generator.get_post_data().decode("utf-8")

        # Check if the unicode value is correctly added
        self.assertIn('Content-Disposition: form-data; name="key1"', post_data)
        self.assertIn("值", post_data)

    def test_add_params_with_file(self):
        # Create a mock file-like object
        mock_file = io.BytesIO(b"file content")
        mock_file.name = "test_file.txt"
        params = {"file": mock_file}

        self.generator.add_params(params)
        post_data = self.generator.get_post_data().decode("utf-8")

        # Check if the file is correctly added
        self.assertIn(
            'Content-Disposition: form-data; name="file"; filename="test_file.txt"',
            post_data,
        )
        self.assertIn("Content-Type: application/octet-stream", post_data)
        self.assertIn("file content", post_data)

    def test_get_post_data(self):
        params = {"key1": "value1"}
        self.generator.add_params(params)
        post_data = self.generator.get_post_data()

        # Check if the post data is not empty
        self.assertGreater(len(post_data), 0)

    def test_boundary_initialization(self):
        # Check if the boundary is initialized correctly
        boundary = self.generator.boundary
        self.assertIsInstance(boundary, int)

    def test_write_method_with_string(self):
        self.generator._write("test")
        post_data = self.generator.get_post_data().decode("utf-8")
        self.assertIn("test", post_data)

    def test_write_method_with_bytes(self):
        self.generator._write(b"test bytes")
        post_data = self.generator.get_post_data().decode("utf-8")
        self.assertIn("test bytes", post_data)

    def test_write_file_method(self):
        # Create a mock file-like object
        mock_file = io.BytesIO(b"file content")
        mock_file.name = "test_file.txt"
        self.generator._write_file(mock_file)

        post_data = self.generator.get_post_data().decode("utf-8")
        self.assertIn("file content", post_data)


if __name__ == "__main__":
    unittest.main()
