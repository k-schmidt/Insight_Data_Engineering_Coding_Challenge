"""
Unit tests for feature 5

Kyle Schmidt
Inisght Data Engineering Coding Challenge
"""
from collections import deque
from datetime import datetime, timedelta
from unittest import TestCase, mock

from src.pkg.feature_5 import feature_5


class TestFeature5(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_dict = {"host": "199.72.81.55",
                             "timestamp": "01/Jul/1995:00:00:01 -0400",
                             "request": "GET /history/apollo/ HTTP/1.0",
                             "http_reply_code": "200",
                             "bytes_transferred": "6245"}
        cls.timestamp = cls.expected_dict["timestamp"]
        cls.timestamp_pattern = "%d/%b/%Y:%H:%M:%S -0400"
        cls.top_n = 6
        cls.datetime_obj = datetime.strptime(cls.expected_dict["timestamp"],
                                             cls.timestamp_pattern)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.deque = deque()
        self.heap = []
        self.time_rollover_queue = deque()

    def tearDown(self):
        pass

    @mock.patch("src.pkg.feature_5.date_to_datetime", side_effect=ValueError)
    def test_return_none_value_error(self, mock_value_error):
        """
        Testing lines 29-31
        Datetime parsing error should skip the ValueError and continue
        """
        max_hour_count = (None, None, None)
        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertIsNone(result)

    def test_empty_queue(self):
        """
        If the queue is empty then we want to initialize the queue
        """
        max_hour_count = (None, None, None)
        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertEqual(len(self.deque), 1)
        self.assertIsNone(result)
        self.assertEqual(self.deque[0], (self.datetime_obj, self.timestamp))

    def test_date_obj_within_t_delta(self):
        """
        Testing lines 33-35
        We keep an initial queue with only the timestamps
        within queue[0] += 60 minutes

        Append to queue if the new timestamp falls within this range
        """
        max_hour_count = (None, None, None)
        self.deque.append((self.datetime_obj, self.timestamp))
        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertEqual(len(self.deque), 2)
        self.assertEqual(self.deque[-1], (self.datetime_obj, self.timestamp))
        self.assertEqual(result, max_hour_count)

    @mock.patch("src.pkg.feature_5.date_to_datetime")
    def test_new_record_greater_than_min_and_max_hour_none(self, mock_datetime_obj):
        """
        Testing lines 51-54
        Creating max_hour_count if it doesn't exist
        """
        max_hour_count = None
        self.deque.append((self.datetime_obj, self.timestamp))
        deque_length = len(self.deque)
        mock_datetime_obj.return_value = self.datetime_obj + timedelta(minutes=70)

        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertEqual(result,
                         (self.datetime_obj, self.timestamp, deque_length))
        self.assertEqual(self.deque[0], (mock_datetime_obj.return_value,
                                         self.expected_dict["timestamp"]))
        self.assertEqual(len(self.time_rollover_queue), 0)

    @mock.patch("src.pkg.feature_5.date_to_datetime")
    def test_new_record_within_min_and_new_max_hour(self, mock_datetime_obj):
        """
        Testing lines 55-61
        Updating max_hour_count if the observed time is the max within given hour
        """
        max_hour_count = (self.datetime_obj + timedelta(minutes=40),
                          "timestamp",
                          0)
        self.deque.append((self.datetime_obj, self.timestamp))
        deque_length = len(self.deque)
        mock_datetime_obj.return_value = self.datetime_obj + timedelta(minutes=70)
        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertEqual(result, (self.datetime_obj,
                                  self.timestamp,
                                  deque_length))

    @mock.patch("src.pkg.feature_5.date_to_datetime")
    def test_popleft_when_equal(self, mock_datetime_obj):
        """
        Testing lines 43 & 44
        Test that the queue continues to pop when there are multiple occurences
        of a timestamp at the beginning of the queue
        """
        max_hour_count = None
        mock_datetime_obj.return_value = self.datetime_obj + timedelta(minutes=70)
        self.deque.append((self.datetime_obj, self.timestamp))
        self.deque.append((self.datetime_obj, self.timestamp))
        deque_length = len(self.deque)
        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertEqual(result, (self.datetime_obj,
                                  self.timestamp,
                                  deque_length))

    @mock.patch("src.pkg.feature_5.date_to_datetime")
    def test_coordinating_queues(self, mock_datetime_obj):
        """
        Testing lines 43-49
        Test that both queues are coordinating together.
        Queue 2 (time_rollover_queue) pops and pushes its value
        onto Queue 1 when its leftmost value becomes in range of the
        first value of Queue 1
        """
        max_hour_count = None
        mock_datetime_obj.return_value = self.datetime_obj + timedelta(minutes=130)
        left_over_queue = self.datetime_obj + timedelta(minutes=40)
        init_rollover_queue = self.datetime_obj + timedelta(minutes=70)
        self.deque.append((self.datetime_obj, self.timestamp))
        self.deque.append((self.datetime_obj, self.timestamp))
        self.deque.append((left_over_queue, "timestamp"))
        deque_length = len(self.deque)
        self.time_rollover_queue.append((init_rollover_queue, "timestamp"))
        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertEqual(result,
                         (self.datetime_obj,
                          self.timestamp,
                          deque_length))
        self.assertEqual(len(self.deque), 2)
        self.assertEqual(self.deque[0], (left_over_queue, "timestamp"))
        self.assertEqual(self.deque[-1], (init_rollover_queue, "timestamp"))
        self.assertEqual(len(self.time_rollover_queue), 1)
        self.assertEqual(self.time_rollover_queue[0],
                         (mock_datetime_obj.return_value,
                          self.timestamp))

    @mock.patch("src.pkg.feature_5.date_to_datetime")
    def test_new_record_greater_than_min_and_new_max_hour(self, mock_datetime_obj):
        """
        Testing lines 62-75
        Push values onto heap if heap is less than top_n

        Push and pop values when the heap becomes == top_n
        """
        max_hour_count = (self.datetime_obj,
                          "timestamp",
                          70)
        self.deque.append((self.datetime_obj + timedelta(minutes=70), "timestamp"))
        deque_length = len(self.deque)
        mock_datetime_obj.return_value = self.datetime_obj + timedelta(minutes=280)
        self.time_rollover_queue.append((self.datetime_obj + timedelta(minutes=140), "timestamp"))
        result = feature_5(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           max_hour_count,
                           self.time_rollover_queue)
        self.assertEqual(len(self.deque), 1)
        self.assertEqual(self.deque[0][0], self.datetime_obj + timedelta(minutes=140))
        self.assertEqual(self.time_rollover_queue[0][0], self.datetime_obj + timedelta(minutes=280))
        self.assertEqual(len(self.time_rollover_queue), 1)
        self.assertEqual(result,
                         (self.datetime_obj + timedelta(minutes=70),
                          "timestamp",
                          deque_length))
        self.assertEqual(self.heap, [(70, "timestamp")])
