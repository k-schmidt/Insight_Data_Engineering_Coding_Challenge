"""
Test Trie and Node

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import unittest

from trie import Node, Trie


class TestTrie(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.node = Node("t", "Insight")
        self.trie = Trie()

    def tearDown(self):
        pass

    def test_node_add_child(self):
        key1 = "e"
        key2 = "g"
        data2 = "Engineering"
        self.node.add_child(key1)
        self.assertEqual(self.node.data, "Insight")
        self.assertEqual(self.node.label, "t")
        self.assertIsNone(self.node[key1].data)
        self.node.add_child(key2, data2)
        self.assertEqual(self.node[key2].data, data2)

    def test_node_increment_priority(self):
        self.node.increment_priority(2)
        self.assertEqual(self.node.count, 2)
        self.node.increment_priority(4)
        self.assertEqual(self.node.count, 6)

    def test_trie_add(self):
        item = "Insight"
        node = self.trie.add(item)
        self.assertEqual(node.data, item)
        self.assertEqual(node.count, 1)
        self.assertEqual(node.label, item[-1])
        self.assertIn("I", self.trie.head)

        item2 = "Integer"
        node2 = self.trie.add(item2)
        self.assertEqual(node2.data, item2)
        self.assertEqual(node2.count, 1)
        self.assertEqual(node2.label, item2[-1])
        self.assertIn("t", self.trie.head["I"]["n"])
        self.assertIn("s", self.trie.head["I"]["n"])

        self.trie.add(item)
        self.assertEqual(node.data, item)
        self.assertEqual(node.count, 2)
        self.assertEqual(node.label, item[-1])
        self.assertIn("I", self.trie.head)
        self.assertIn("t", self.trie.head["I"]["n"])
        self.assertIn("s", self.trie.head["I"]["n"])

        item3 = "Trie"
        node3 = self.trie.add(item3)
        self.assertEqual(node3.data, item3)
        self.assertEqual(node3.count, 1)
        self.assertEqual(node3.label, item3[-1])
        self.assertIn("I", self.trie.head)
        self.assertIn("t", self.trie.head["I"]["n"])
        self.assertIn("s", self.trie.head["I"]["n"])
        self.assertIn("T", self.trie.head)
        self.assertIn("r", self.trie.head["T"])
        self.assertIn("i", self.trie.head["T"]["r"])

        print(self.trie.head)
        print(node)
