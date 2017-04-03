"""
Trie Implementation

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from typing import Optional


class Node(dict):

    def __init__(self, label: Optional[str]=None):
        self.label = label
        self.count = 0
        self.is_in_heap = False

    def add_child(self, key: str):
        self[key] = Node(key)

    def increment_priority(self, priority_incrementer: int):
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
        self.head = Node()

    def add(self, item: str, priority_incrementer: int=1):
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
