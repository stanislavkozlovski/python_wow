"""
Test the helper functions in utils/helper.py
"""
import unittest

from utils.helper import parse_int


class TestUtils(unittest.TestCase):
    def test_parse_int_valid_numbers(self):
        self.assertIsNotNone(parse_int(1))
        self.assertTrue(isinstance(parse_int(5), int))
        self.assertEqual(parse_int(1), 1)
        self.assertEqual(parse_int(3), 3)
        self.assertEqual(parse_int(5), 5)
        self.assertEqual(parse_int(215), 215)

    def test_parse_int_invalid_numbers(self):
        """
        It should convert every invalid integer to 0
        """
        self.assertEqual(parse_int(2.1), 2)
        self.assertEqual(parse_int(None), 0)
        self.assertEqual(parse_int('aa'), 0)
        self.assertEqual(parse_int([]), 0)


if __name__ == '__main__':
    unittest.main()
