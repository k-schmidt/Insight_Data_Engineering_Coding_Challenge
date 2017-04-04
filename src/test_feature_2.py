"""
Test Feature 2

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import os
import unittest
from unittest import mock

from config import PATH_TEST_ACTIVE_RESOURCES
from feature_2 import feature_2, write_top_n_heap_to_outfile
from trie import Node


class TestFeature2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        open(PATH_TEST_ACTIVE_RESOURCES, 'w').close()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.failing_parsed_line = {"request": "GT /history/apollo/ HTTP/1.0"}
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

    def tearDown(self):
        os.remove(PATH_TEST_ACTIVE_RESOURCES)

    @mock.patch("feature_2.Trie")
    def test_feature_2_return_none(self, mock_trie):
        mock_trie_obj = mock_trie.return_value
        self.assertIsNone(
            feature_2(mock_trie_obj,
                      self.node_heap,
                      self.failing_parsed_line,
                      self.top_n))

    def test_write_top_n_heap_to_outfile(self):
        """
        Integration test for writing top_n heap to file
        """
        write_top_n_heap_to_outfile(self.node_heap,
                                    PATH_TEST_ACTIVE_RESOURCES,
                                    self.top_n)

        with open(PATH_TEST_ACTIVE_RESOURCES, 'r') as results:
            result = [line.strip()
                      for line
                      in results.readlines()]
            sorted_node_heap = [item.strip()
                                for priority, node, item
                                in sorted(self.node_heap, reverse=True)][:self.top_n]
            self.assertEqual(result, sorted_node_heap)
            self.assertEqual(len(result), self.top_n)
