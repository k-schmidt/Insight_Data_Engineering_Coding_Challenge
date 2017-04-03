"""
Feature 2

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import heapq
from typing import List, Tuple

from common_methods import (append_to_heap,
                            format_bytes,
                            is_valid_crud)
from trie import Node, Trie


def feature_2(resource_trie: Trie,
              most_active_heap: List[Tuple[int, Node]],
              parsed_line: str,
              top_n: int) -> None:
    request = parsed_line["request"]
    if not is_valid_crud(request):  # Skip poorly formatted requests
        return
    split_request = request.split()
    resource = split_request[1]
    priority_incrementer = format_bytes(parsed_line)
    node = resource_trie.add(resource, priority_incrementer)
    append_to_heap(node, most_active_heap, top_n)
