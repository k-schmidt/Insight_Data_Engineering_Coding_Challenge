"""
Trie Implementation
"""
from typing import Optional, Union


class Node(dict):

    def __init__(self, label: Optional[str]=None, data: Optional[int]=None):
        self.label = label
        self.data = data
        self.count = 0

    def add_child(self, key: str, data: Optional[str]=None):
        self[key] = Node(key, data)


class Trie:

    def __init__(self):
        self.head = Node()

    def add(self, item):
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

        current_node.count += 1
        current_node.data = item
        return current_node
