"""
Test Feature 2

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import unittest
from unittest import mock

from feature_2 import feature_2
from trie import Node


class TestFeature2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

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
        self.node_heap = [(self.node_in_heap.count, self.node_in_heap),
                          (2, Node("g"), "Engineering"),
                          (3, Node("s"), "Statistics"),
                          (4, Node("h"), "Math"),
                          (5, Node("n"), "Econ"),
                          (6, Node("e"), "Science"),
                          (7, Node("t"), "Insight")]

    def tearDown(self):
        pass

    @mock.patch("feature_2.Trie")
    def test_feature_2_return_none(self, mock_trie):
        mock_trie_obj = mock_trie.return_value
        self.assertIsNone(
            feature_2(mock_trie_obj,
                      self.node_heap,
                      self.failing_parsed_line,
                      self.top_n))
