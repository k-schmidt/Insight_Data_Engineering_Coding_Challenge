"""
Unit tests for feature 4

Kyle Schmidt
Inisght Data Engineering Coding Challenge
"""
from collections import defaultdict, deque
from datetime import datetime, timedelta
from unittest import TestCase

from src.feature_4 import feature_4


class TestFeature4(TestCase):

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

    def tearDown(self):
        pass

    def test_host_in_blocked_users(self):
        """
        Testing lines 24-26
        If the host is in the blocked users and the timestamp is within the 5 minute
        range then we want to return True
        """
        logged_time = self.datetime_obj - timedelta(minutes=1)
        blocked_users = {self.expected_dict["host"]: logged_time}
        user_dict = {}
        self.assertTrue(
            feature_4(self.expected_dict,
                      user_dict,
                      blocked_users))

    def test_pop_blocked_and_append(self):
        """
        Testing lines 28-33
        If the host is in the blocked users and the timestamp is over the 5 minute
        range then we pop the host from the blocked users

        If the new record is a failed login (http: 401) then we append the host
        and timestamp to the failed login dictionary
        """
        logged_time = self.datetime_obj - timedelta(minutes=6)
        blocked_users = {self.expected_dict["host"]: logged_time}
        user_dict = defaultdict(deque)
        self.expected_dict["http_reply_code"] = "401"
        feature_4(self.expected_dict,
                  user_dict,
                  blocked_users)
        self.assertNotIn(self.expected_dict["host"],
                         blocked_users)
        self.assertIn(self.expected_dict["host"],
                      user_dict)
        self.assertEqual(len(user_dict[self.expected_dict["host"]]),
                         1)
        self.assertEqual(user_dict[self.expected_dict["host"]][0],
                         self.datetime_obj)

    def test_pop_from_user_dict_http_not_401(self):
        """
        Testing line 45 & 46
        If the user is not in the blocked users and did not have a failed login
        then we pop the host from the failed login dictionary
        """
        blocked_users = {}
        user_dict = defaultdict(deque)
        user_dict[self.expected_dict["host"]].append(
            self.datetime_obj - timedelta(seconds=10))
        feature_4(self.expected_dict,
                  user_dict,
                  blocked_users)
        self.assertNotIn(self.expected_dict["host"],
                         user_dict)

    def test_pop_older_timestamps_for_user(self):
        """
        Testing lines 36-41
        If the status code is 401 and if the user had two failed logins and
        then waited greater than 20 seconds to login
        again then we will want to pop those records that are older than 20 seconds
        for that user in the failed login dictionary and append the new record
        """
        blocked_users = {}
        user_dict = defaultdict(deque)
        logged_time1 = self.datetime_obj - timedelta(seconds=25)
        logged_time2 = self.datetime_obj - timedelta(seconds=23)
        logged_time3 = self.datetime_obj - timedelta(seconds=5)
        for time in [logged_time1, logged_time2, logged_time3]:
            user_dict[self.expected_dict["host"]].append(time)
        self.expected_dict["http_reply_code"] = "401"
        feature_4(self.expected_dict,
                  user_dict,
                  blocked_users)
        self.assertNotIn(logged_time1,
                         user_dict[self.expected_dict["host"]])
        self.assertNotIn(logged_time2,
                         user_dict[self.expected_dict["host"]])
        self.assertIn(logged_time3,
                      user_dict[self.expected_dict["host"]])
        self.assertIn(self.datetime_obj,
                      user_dict[self.expected_dict["host"]])
        self.assertEqual(len(user_dict[self.expected_dict["host"]]),
                         2)

    def test_pop_older_timestamps_and_append_blocked_user(self):
        """
        Testing lines 36-44
        If the status code is 401 and if the user had two failed logins and
        then waited greater than 20 seconds to login
        again then we will want to pop those records that are older than 20 seconds
        for that user in the failed login dictionary and append the new record

        If the failed login count for that user becomes 3 after appending the new record
        then we will pop the user from the failed login dictionary
        and append the host and its most recent failed timestamp to the blocked user dictionary
        """
        blocked_users = {}
        user_dict = defaultdict(deque)
        logged_time1 = self.datetime_obj - timedelta(seconds=25)
        logged_time2 = self.datetime_obj - timedelta(seconds=23)
        logged_time3 = self.datetime_obj - timedelta(seconds=5)
        logged_time4 = self.datetime_obj - timedelta(seconds=3)
        for time in [logged_time1, logged_time2, logged_time3, logged_time4]:
            user_dict[self.expected_dict["host"]].append(time)
        self.expected_dict["http_reply_code"] = "401"
        feature_4(self.expected_dict,
                  user_dict,
                  blocked_users)
        self.assertNotIn(self.expected_dict["host"],
                         user_dict)
        self.assertNotIn(logged_time1,
                         user_dict[self.expected_dict["host"]])
        self.assertNotIn(logged_time2,
                         user_dict[self.expected_dict["host"]])
        self.assertIn(self.expected_dict["host"],
                      blocked_users)
        self.assertEqual(blocked_users[self.expected_dict["host"]],
                         self.datetime_obj)
