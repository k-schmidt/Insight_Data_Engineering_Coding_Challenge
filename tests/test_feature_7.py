"""
Unit tests for feature 7

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from collections import defaultdict
from datetime import datetime
from unittest import TestCase, mock

from src.pkg.feature_7 import (add_day_count_to_dict,
                               datetime_obj_to_weekday_name)


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
        self.popular_days = defaultdict(int)

    def tearDown(self):
        pass

    def test_datetime_obj_to_weekday_name(self):
        self.assertEqual("Saturday",
                         datetime_obj_to_weekday_name(self.datetime_obj))

    @mock.patch("src.pkg.feature_7.datetime_obj_to_weekday_name", return_value="Monday")
    def test_add_day_count_to_dict(self, mock_weekday_str):
        add_day_count_to_dict(self.popular_days,
                              self.expected_dict)
        self.assertIn(mock_weekday_str.return_value,
                      self.popular_days)
        self.assertEqual(self.popular_days[mock_weekday_str.return_value], 1)
