"""
Test Trie and Node

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import unittest

from src.pkg.trie import Node, Trie


class TestTrie(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.node = Node("t")
        self.trie = Trie()

    def tearDown(self):
        pass

    def test_node_add_child(self):
        key1 = "e"
        key2 = "g"
        self.node.add_child(key1)
        self.assertEqual(self.node.label, "t")
        self.assertIn("e", self.node)
        self.node.add_child(key2)
        self.assertIn("g", self.node)

    def test_node_increment_priority(self):
        self.node.increment_priority(2)
        self.assertEqual(self.node.count, 2)
        self.node.increment_priority(4)
        self.assertEqual(self.node.count, 6)

    def test_trie_add(self):
        item = "Insight"
        node, returned_item = self.trie.add(item)
        self.assertEqual(item, returned_item)
        self.assertEqual(node.count, 1)
        self.assertEqual(node.label, item[-1])
        self.assertIn("I", self.trie.head)

        item2 = "Integer"
        node2, returned_item_2 = self.trie.add(item2)
        self.assertEqual(returned_item_2, item2)
        self.assertEqual(node2.count, 1)
        self.assertEqual(node2.label, item2[-1])
        self.assertIn("t", self.trie.head["I"]["n"])
        self.assertIn("s", self.trie.head["I"]["n"])

        self.trie.add(item)
        self.assertEqual(node.count, 2)
        self.assertEqual(node.label, item[-1])
        self.assertIn("I", self.trie.head)
        self.assertIn("t", self.trie.head["I"]["n"])
        self.assertIn("s", self.trie.head["I"]["n"])

        item3 = "Trie"
        node3, returned_item3 = self.trie.add(item3)
        self.assertEqual(returned_item3, item3)
        self.assertEqual(node3.count, 1)
        self.assertEqual(node3.label, item3[-1])
        self.assertIn("I", self.trie.head)
        self.assertIn("t", self.trie.head["I"]["n"])
        self.assertIn("s", self.trie.head["I"]["n"])
        self.assertIn("T", self.trie.head)
        self.assertIn("r", self.trie.head["T"])
        self.assertIn("i", self.trie.head["T"]["r"])
