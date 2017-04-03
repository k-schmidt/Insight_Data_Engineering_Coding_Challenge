"""
Feature 2

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import heapq
from typing import Dict, List, Tuple

from common_methods import (append_to_heap,
                            format_bytes,
                            is_valid_crud)
from trie import Node, Trie


def feature_2(resource_trie: Trie,
              most_active_heap: List[Tuple[int, Node]],
              parsed_line: Dict[str, str],
              top_n: int) -> None:
    request = parsed_line["request"]
    if not is_valid_crud(request):  # Skip poorly formatted requests
        return
    split_request = request.split()
    resource = split_request[1]
    priority_incrementer = format_bytes(parsed_line)
    node, item = resource_trie.add(resource, priority_incrementer)
    append_to_heap(node, item, most_active_heap, top_n)


def write_top_n_heap_to_outfile(heap,
                                outfile,
                                top_n):
    n_largest = heapq.nlargest(top_n, heap)
    with open(outfile, 'w') as writer:
        for _, node, data in n_largest:
            writer.write(data + "\n")
