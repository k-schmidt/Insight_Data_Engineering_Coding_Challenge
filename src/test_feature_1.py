"""
Unit tests for feature 1

Kyle Schmidt
Inisght Data Engineering Coding Challenge
"""
from unittest import TestCase

from config import PATH_TEST_ACTIVE_ADDRESSES
from feature_1 import write_top_n_heap_to_outfile
from trie import Node


class TestCommonMethods(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

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

    def tearDown(self):
        pass

    def test_write_top_n_heap_to_outfile(self):
        """
        Integration test of writing top_n heap to file
        """
        write_top_n_heap_to_outfile(self.node_heap,
                                    PATH_TEST_ACTIVE_ADDRESSES,
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
