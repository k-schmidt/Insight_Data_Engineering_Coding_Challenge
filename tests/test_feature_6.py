"""
Unit tests for feature 6

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from collections import defaultdict
from datetime import datetime
from unittest import TestCase, mock

from src.pkg.feature_6 import format_hour_str, add_hour_to_dict


class TestFeature6(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.expected_dict = {"host": "199.72.81.55",
                              "timestamp": "01/Jul/1995:00:00:01 -0400",
                              "request": "GET /history/apollo/ HTTP/1.0",
                              "http_reply_code": "200",
                              "bytes_transferred": "6245"}
        self.timestamp = self.expected_dict["timestamp"]
        self.timestamp_pattern = "%d/%b/%Y:%H:%M:%S -0400"
        self.top_n = 6
        self.datetime_obj = datetime.strptime(self.expected_dict["timestamp"],
                                              self.timestamp_pattern)
        self.common_times = defaultdict(int)

    def tearDown(self):
        pass

    @mock.patch("src.pkg.feature_6.format_hour_str", return_value="timestamp")
    def test_incrementer(self, mock_timestamp_str):
        add_hour_to_dict(self.common_times,
                         self.expected_dict)
        self.assertIn(mock_timestamp_str.return_value, self.common_times)
        self.assertEqual(self.common_times["timestamp"], 1)

    def test_format_hour_str(self):
        self.assertEqual(format_hour_str(self.datetime_obj),
                         "00:00:00")
