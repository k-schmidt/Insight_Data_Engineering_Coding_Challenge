"""
Unit tests for common methods

Kyle Schmidt
Inisght Data Engineering Coding Challenge
"""
from datetime import datetime
import os
import re
import unittest
from unittest import mock

from config import (PATH_TEST_DATA,
                    PATH_TEST_ACTIVE_ADDRESSES,
                    PATH_TEST_ACTIVE_RESOURCES,
                    PATH_TEST_ACTIVE_TIME,
                    PATH_BLOCKED_USER_LOG,
                    PATH_TEST_DIR)
from common_methods import (gen_data_rows,
                            append_to_heap,
                            date_to_datetime,
                            parse_log_row,
                            is_valid_crud,
                            format_bytes)
from trie import Node


class TestCommonMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log_line = """199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245\n"""
        cls.failing_log_line = """199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] “POST /login HTTP/1.0” 401 1420"""
        cls.regex_pattern = r"(?P<host>(.*)) - - \[(?P<timestamp>(.*))\] \"(?P<request>(.*))\" (?P<http_reply_code>(\d{3})) (?P<bytes_transferred>(.*))"
        cls.compiled_regex = re.compile(cls.regex_pattern)
        cls.expected_dict = {"host": "199.72.81.55",
                             "timestamp": "01/Jul/1995:00:00:01 -0400",
                             "request": "GET /history/apollo/ HTTP/1.0",
                             "http_reply_code": "200",
                             "bytes_transferred": "6245"}
        cls.timestamp_pattern = "%d/%b/%Y:%H:%M:%S -0400"
        if not os.path.exists(PATH_TEST_DIR):
            os.makedirs(PATH_TEST_DIR)
        open(PATH_TEST_ACTIVE_ADDRESSES, 'w').close()
        open(PATH_TEST_ACTIVE_RESOURCES, 'w').close()
        open(PATH_TEST_ACTIVE_TIME, 'w').close()

    @classmethod
    def tearDownClass(cls):
        os.remove(PATH_TEST_ACTIVE_ADDRESSES)
        os.remove(PATH_TEST_ACTIVE_RESOURCES)
        os.remove(PATH_TEST_ACTIVE_TIME)

    def setUp(self):
        self.node_in_heap = Node("a")
        self.node_word = "Data"
        self.node_in_heap.is_in_heap = True
        self.node_in_heap.count = 1
        self.top_n = 5
        self.node_heap = [(self.node_in_heap.count, self.node_in_heap, self.node_word),
                          (2, Node("g"), "Engineering"),
                          (3, Node("s"), "Statistics"),
                          (4, Node("h"), "Math"),
                          (5, Node("n"), "Econ"),
                          (6, Node("e"), "Science"),
                          (7, Node("t"), "Insight")]
        self.data_heap = [(1, "i"),
                          (2, "n"),
                          (3, "s"),
                          (4, "i"),
                          (5, "g"),
                          (6, "h"),
                          (7, "t")]

    def tearDown(self):
        pass

    def test_gen_data_rows(self):
        self.assertEqual(self.log_line,
                         next(gen_data_rows(PATH_TEST_DATA)))

    def test_passing_parse_log_row(self):
        self.assertEqual(parse_log_row(self.log_line,
                                       self.compiled_regex),
                         self.expected_dict)

    def test_failing_parse_log_row(self):
        self.assertRaises(AttributeError,
                          parse_log_row,
                          self.failing_log_line,
                          self.compiled_regex)

    def test_is_valid_crud(self):
        passing_request = "DELETED"
        failing_request = "DLETE"
        self.assertTrue(is_valid_crud(passing_request))
        self.assertFalse(is_valid_crud(failing_request))

    def test_format_bytes(self):
        parsed_line = {}
        with mock.patch.dict(parsed_line, {"bytes_transferred": "-"}):
            self.assertEqual(format_bytes(parsed_line),
                             0)

        with mock.patch.dict(parsed_line, {"bytes_transferred": "200"}):
            self.assertEqual(format_bytes(parsed_line),
                             200)

    def test_date_to_datetime(self):
        datetime_obj = datetime.strptime(self.expected_dict["timestamp"],
                                         self.timestamp_pattern)
        failing_timestamp = "01/Jul/1995:00:00:01"
        self.assertEqual(date_to_datetime(self.expected_dict["timestamp"]),
                         datetime_obj)
        self.assertRaises(ValueError,
                          date_to_datetime,
                          failing_timestamp)

    @unittest.skip("")
    def test_write_top_n_heap_to_outfile(self):
        write_top_n_heap_to_outfile(self.node_heap,
                                    PATH_TEST_ACTIVE_ADDRESSES,
                                    self.top_n,
                                    sep=",")
        write_top_n_heap_to_outfile(self.node_heap,
                                    PATH_TEST_ACTIVE_RESOURCES,
                                    self.top_n)
        write_top_n_heap_to_outfile(self.data_heap,
                                    PATH_TEST_ACTIVE_TIME,
                                    self.top_n,
                                    sep=",")
        with open(PATH_TEST_ACTIVE_ADDRESSES, 'r') as results:
            result = [line.strip()
                      for line
                      in results.readlines()]
            sorted_node_heap = [",".join([item, str(priority)]).strip()
                                for priority, node, item
                                in sorted(self.node_heap, reverse=True)][:self.top_n]
            self.assertEqual(result, sorted_node_heap)
            self.assertEqual(len(result), self.top_n)

        with open(PATH_TEST_ACTIVE_TIME, 'r') as results:
            result = [line.strip()
                      for line
                      in results.readlines()]
            sorted_heap = [",".join([data, str(priority)]).strip()
                           for priority, data
                           in sorted(self.data_heap, reverse=True)][:self.top_n]
            self.assertEqual(result, sorted_heap)
            self.assertEqual(len(result), self.top_n)

        with open(PATH_TEST_ACTIVE_RESOURCES, 'r') as results:
            result = [line.strip() for line in results.readlines()]
            sorted_heap = [item.strip()
                           for _, node, item
                           in sorted(self.node_heap, reverse=True)][:self.top_n]
            self.assertEqual(result, sorted_heap)
            self.assertEqual(len(result), self.top_n)

    def test_heap_push_append_to_heap(self):
        test_node = Node("a")
        word = "Nasa"
        test_node.count = 100
        top_n = 10

        append_to_heap(test_node,
                       word,
                       self.node_heap,
                       top_n)
        self.assertIn((test_node.count, test_node, word),
                      self.node_heap)
        self.assertTrue(test_node.is_in_heap)

    @mock.patch("common_methods.heapq.heapify")
    def test_node_in_heap_append_to_heap(self, mock_heapify):
        top_n = 10
        self.assertEqual(self.node_in_heap.count, 1)
        self.node_in_heap.count = 100
        append_to_heap(self.node_in_heap,
                       self.node_word,
                       self.node_heap,
                       top_n)
        self.assertIn((self.node_in_heap.count, self.node_in_heap, self.node_word),
                      self.node_heap)
        self.assertTrue(self.node_in_heap.is_in_heap)
        self.assertEqual(self.node_in_heap.count, 100)
        mock_heapify.assert_called_with(self.node_heap)

    @mock.patch("common_methods.heapq.heapify")
    def test_append_node_in_heap_larger_than_n(self, mock_heapify):
        self.node_in_heap.count = 100
        append_to_heap(self.node_in_heap,
                       self.node_word,
                       self.node_heap,
                       self.top_n)
        self.assertIn((self.node_in_heap.count, self.node_in_heap, self.node_word),
                      self.node_heap)
        mock_heapify.assert_called_with(self.node_heap)

    def test_append_node_heap_larger_than_n(self):
        test_node = Node("a")
        test_node.count = 100
        word = "Nasa"
        append_to_heap(test_node,
                       word,
                       self.node_heap,
                       self.top_n)
        self.assertIn((test_node.count, test_node, word),
                      self.node_heap)
        self.assertTrue(test_node.is_in_heap)
        self.assertFalse(self.node_in_heap)

    @mock.patch("common_methods.heapq.heappushpop")
    def test_append_node_heap_heappushpop(self, mock_heappushpop):
        mock_heappushpop.return_value = (self.node_in_heap.count,
                                         self.node_in_heap,
                                         self.node_word)
        test_node = Node("a")
        test_node.count = 100
        word = "Nasa"

        append_to_heap(test_node,
                       word,
                       self.node_heap,
                       self.top_n)
        mock_heappushpop.assert_called_with(self.node_heap,
                                            (test_node.count, test_node, word))
