import unittest
from unittest.mock import patch
from src.utils import Utils

# The tests use mock to imitate user input

class TestUtils(unittest.TestCase):
    @patch("builtins.input", side_effect=["y"])
    def test_validate_input_yes(self, mock_input):
        result = Utils.validate_input("Do you want to proceed?")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["Y"])
    def test_validate_input_upper_yes(self, mock_input):
        result = Utils.validate_input("Do you want to proceed?")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["n"])
    def test_validate_input_no(self, mock_input):
        result = Utils.validate_input("Do you want to proceed?")
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["N"])
    def test_validate_input_upper_no(self, mock_input):
        result = Utils.validate_input("Do you want to proceed?")
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["maybe", "Y"])
    def test_validate_input_invalid_then_yes(self, mock_input):
        result = Utils.validate_input("Do you want to proceed?")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["123", "n"])
    def test_validate_input_invalid_then_no(self, mock_input):
        result = Utils.validate_input("Do you want to proceed?")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()