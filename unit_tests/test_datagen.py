import os
import random
import unittest
from unittest.mock import patch, MagicMock, call

# The tests use mocks to imitate the system calls without executing them on the file system

class TestDeleteData(unittest.TestCase):
    def setUp(self):
        self.test_directory = "/path/to/test_directory"

    @patch("os.listdir")
    @patch("os.remove")
    def test_delete_data(self, mock_remove, mock_listdir):
        mock_listdir.return_value = ["file1.csv", "file2.csv", "file3.csv"]

        class TestClass:
            def __init__(self, directory):
                self.directory = directory

            def delete_data(self):
                for file in os.listdir(self.directory):
                    os.remove(os.path.join(self.directory, file))
                    print("Removed file {}".format(file))

        instance = TestClass(self.test_directory)
        instance.delete_data()
        mock_listdir.assert_called_once_with(self.test_directory)
        expected_calls = [
            call(os.path.join(self.test_directory, "file1.csv")),
            call(os.path.join(self.test_directory, "file2.csv")),
            call(os.path.join(self.test_directory, "file3.csv")),
        ]
        mock_remove.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_remove.call_count, 3)

    @patch("os.listdir")
    @patch("os.remove")
    def test_delete_data_empty_directory(self, mock_remove, mock_listdir):
        mock_listdir.return_value = []

        class TestClass:
            def __init__(self, directory):
                self.directory = directory

            def delete_data(self):
                for file in os.listdir(self.directory):
                    os.remove(os.path.join(self.directory, file))
                    print("Removed file {}".format(file))

        instance = TestClass(self.test_directory)
        instance.delete_data()
        mock_listdir.assert_called_once_with(self.test_directory)
        mock_remove.assert_not_called()

if __name__ == '__main__':
    unittest.main()