"""
Trie Implementation

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from typing import Optional, Tuple


class Node(dict):

    def __init__(self, label: Optional[str]=None):
        """
        Node class representing a value in the Trie class.
        Node inherits from dict providing dictionary functionality
        while being able to store additional data

        Attributes:
            label: Character of word within Trie
            count: Number of times the word has been seen
                   Count is only incremented when we reach the end
                   of a word.
            is_in_heap: Boolean indicator letting us know when to
                        traverse a heap looking for the node
        """
        self.label = label
        self.count = 0  # type: int
        self.is_in_heap = False  # type: bool

    def add_child(self, key: str) -> None:
        """
        Add a value to the Node which itself is another Node

        Arguments:
            key: Character of word
        """
        self[key] = Node(key)

    def increment_priority(self, priority_incrementer: int) -> None:
        """
        Nodes will also be stored in a heap and we need to
        be able to update a Nodes priority within that heap

        Priority Incrementer tells us how much to increment the priority by

        Arguments:
            priority_incrementer: Number to increment instance attribute count
        """
        self.count += priority_incrementer

    def __repr__(self):
        if not self.keys():
            return "Node(label={}, count={}, is_in_heap={}"\
                .format(self.label,
                        self.count,
                        self.is_in_heap)
        else:
            return "Node({})".format([(key, value)
                                      for key, value
                                      in self.items()])


class Trie:

    def __init__(self):
        """
        Class used as an ADT of Trie

        A Trie contains Nodes which contain characters of a word and pointers
        to additonal characters of words.

        Attributes:
            head: Empty Node instance
        """
        self.head = Node()  # type: Node

    def add(self, item: str, priority_incrementer: int=1) -> Tuple[Node, str]:
        """
        Add a word to the Trie by traversing the characters of that word.
        If the word is already in the Trie then we will visit of the
        Nodes representing that word.
        Otherwise we will create new Nodes to represent that word.
        Finally we will increment the counter for that word.

        Arguments:
            item: The word to add to the Trie
            priority_incrementer: Number to increase the Node's count attribute

        Returns:
            Node instance representing the last character of the word and
            the word itself
        """
        current_node = self.head
        item_finished = True

        for index in range(len(item)):
            char = item[index]
            if char in current_node:
                current_node = current_node[char]
            else:
                item_finished = False
                break

        if not item_finished:
            while index < len(item):
                char = item[index]
                current_node.add_child(char)
                current_node = current_node[char]
                index += 1

        current_node.increment_priority(priority_incrementer)
        return current_node, item
