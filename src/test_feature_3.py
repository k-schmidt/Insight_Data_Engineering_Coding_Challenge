"""
Unit tests for feature 3

Kyle Schmidt
Inisght Data Engineering Coding Challenge
"""
from collections import deque
from datetime import datetime, timedelta
from unittest import TestCase, mock

from config import PATH_TEST_ACTIVE_TIME
from feature_3 import feature_3, write_top_n_heap_to_outfile, exhaust_queue


class TestFeature3(TestCase):

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
        self.data_heap = [(1, "i"),
                          (2, "n"),
                          (3, "s"),
                          (4, "i"),
                          (5, "g"),
                          (6, "h"),
                          (7, "t")]

    def tearDown(self):
        pass

    @mock.patch("feature_3.date_to_datetime", side_effect=ValueError)
    def test_return_none_value_error(self, mock_value_error):
        """
        Testing lines 25-28
        Datetime parsing error should skip the ValueError and return None
        """
        result = feature_3(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
                           self.time_rollover_queue)
        self.assertIsNone(result)

    def test_empty_queue(self):
        """
        Testing lines 29-31
        If the queue is empty then we want to initialize the queue
        """
        result = feature_3(self.deque,
                           self.heap,
                           self.expected_dict,
                           self.top_n,
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
        self.deque.append((self.datetime_obj, self.timestamp))
        feature_3(self.deque,
                  self.heap,
                  self.expected_dict,
                  self.top_n,
                  self.time_rollover_queue)
        self.assertEqual(len(self.deque), 2)
        self.assertEqual(self.deque[-1], (self.datetime_obj, self.timestamp))

    @mock.patch("feature_3.exhaust_queue")
    @mock.patch("feature_3.date_to_datetime")
    def test_new_record_greater_than_min(self,
                                         mock_datetime_obj,
                                         mock_exhaust_queue):
        """
        Testing lines 51-54
        Initialize max hour count for that hour.
        We only want to log observations within an hour once.
        We keep max hour count in order to ensure that we don't double
        count observations within that hour.

        It is possible (and does occur) where a single hour is the most popular
        over the entire range of data and therefore every top_n would be a minute
        within that hour
        """
        self.deque.append((self.datetime_obj, self.timestamp))
        mock_datetime_obj.return_value = self.datetime_obj + timedelta(
            minutes=70)

        feature_3(self.deque,
                  self.heap,
                  self.expected_dict,
                  self.top_n,
                  self.time_rollover_queue)
        self.assertIn((mock_datetime_obj.return_value,
                       self.timestamp),
                      self.time_rollover_queue)
        mock_exhaust_queue.assert_called_with(self.deque,
                                              self.heap,
                                              self.top_n,
                                              self.time_rollover_queue)

    def test_exhaust_queue_one_element(self):
        """
        Testing 107-111 doesn't execute
        Push item to heap once it is popped from queue
        """
        self.deque.append((self.datetime_obj, self.timestamp))
        exhaust_queue(self.deque,
                      self.heap,
                      self.top_n,
                      self.time_rollover_queue)
        self.assertEqual(len(self.deque),
                         0)
        self.assertEqual(self.heap[0],
                         (1, self.timestamp))
        self.assertEqual(len(self.time_rollover_queue),
                         0)

    def test_exhaust_queue_time_rollover(self):
        """
        Testing lines 107-111
        Testing coordinating queues between queue and time_rollover queue
        """
        self.deque.append((self.datetime_obj, self.timestamp))
        self.time_rollover_queue.append((self.datetime_obj, self.timestamp))
        self.time_rollover_queue.append((self.datetime_obj + timedelta(minutes=70),
                                         self.timestamp))
        exhaust_queue(self.deque,
                      self.heap,
                      self.top_n,
                      self.time_rollover_queue)
        self.assertEqual(len(self.deque),
                         1)
        self.assertEqual(self.heap[0],
                         (1, self.timestamp))
        self.assertEqual((len(self.time_rollover_queue)),
                         1)

    def test_exhaust_queue_heappushpop(self):
        """
        Testing lines 118-121
        If we find a new element that should be in the heap
        and our heap is larger than top_n then we will pop
        the smallest from the heap and push the new element
        into its correct position.
        """
        self.deque.append((self.datetime_obj, self.timestamp))
        self.deque.append((self.datetime_obj + timedelta(minutes=20), self.timestamp))
        deque_length = len(self.deque)
        first_heap_element = self.data_heap[0]
        self.time_rollover_queue.append((self.datetime_obj, self.timestamp))
        self.time_rollover_queue.append((self.datetime_obj + timedelta(minutes=70),
                                         self.timestamp))
        exhaust_queue(self.deque,
                      self.data_heap,
                      self.top_n,
                      self.time_rollover_queue)
        self.assertIn((deque_length, self.timestamp),
                      self.data_heap)
        self.assertNotIn(first_heap_element,
                         self.data_heap)

    def test_write_top_n_heap_to_outfile(self):
        """
        Integration test of writing top_n heap to file
        """
        write_top_n_heap_to_outfile(self.data_heap,
                                    PATH_TEST_ACTIVE_TIME,
                                    self.top_n,
                                    sep=",")
        with open(PATH_TEST_ACTIVE_TIME, 'r') as results:
            result = [line.strip()
                      for line
                      in results.readlines()]
            sorted_heap = [",".join([data, str(priority)]).strip()
                           for priority, data
                           in sorted(self.data_heap, reverse=True)][:self.top_n]
            self.assertEqual(result, sorted_heap)
            self.assertEqual(len(result), self.top_n)
