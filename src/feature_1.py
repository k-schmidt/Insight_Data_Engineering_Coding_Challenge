"""
Feature 1

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import heapq
from typing import List, Tuple

from common_methods import append_to_heap
from trie import Node, Trie


def feature_1(host_trie: Trie,
              most_active_heap: List[Tuple[int, Node]],
              parsed_line: str,
              top_n: int) -> None:

    node, item = host_trie.add(parsed_line["host"])
    append_to_heap(node, item, most_active_heap, top_n)


def write_top_n_heap_to_outfile(heap,
                                outfile,
                                top_n,
                                sep=","):
    n_largest = heapq.nlargest(top_n, heap)
    with open(outfile, 'w') as writer:
        for priority, node, item in n_largest:
            writer.write(sep.join([item, str(priority)]) + "\n")
