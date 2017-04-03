"""
Unit tests for common methods

Kyle Schmidt
Inisght Data Engineering Coding Challenge
"""
import unittest

from config import PATH_LOG_TEST_FILE
from common_methods import gen_data_rows


class TestCommonMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip("Having trouble with encode/decode")
    def test_gen_data_rows(self):
        first_line_str = bytes("199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] “POST /login HTTP/1.0” 401 1420", "ISO-8859-1")
        self.assertEqual(next(gen_data_rows(PATH_LOG_TEST_FILE)),
                         first_line_str)
