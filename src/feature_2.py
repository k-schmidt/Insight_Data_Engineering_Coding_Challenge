"""
Feature 2

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import heapq
from typing import Dict, List, Tuple

from .pkg.common_methods import (append_to_heap,
                                 format_bytes,
                                 is_valid_crud)
from .pkg.trie import Node, Trie


def feature_2(resource_trie: Trie,
              most_active_heap: List[Tuple[int, Node]],
              parsed_line: Dict[str, str],
              top_n: int) -> None:
    """
    Identify the top 10 most resources that consume the most
    bandwidth on the site.

    We append the resource to a Trie
    and within the last node of the Trie for that resource
    we keep track of the resource total bytes and whether it is in the heap.
    We maintain a heap for easy access to the minumum element of the top_n
    resources.

    If the nodes is in the heap then we do a linear traversal to find it
    and update its priority.

    Otherwise we append the node to the heap and pop the minimum element of the heap
    if the heap is greater than top_n.

    Arguments:
        resource_trie: Trie to hold each character that makes up a resource
        most_active_heap: Heap to store top_n resources
        parsed_line: Dictionary of parsed log line
        top_n: Number of items to store in most_active_heap
    """
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
    """
    Write the data for the top_n of heap to outfile,
    ignoring their priorities

    Arguments:
        heap: Heap of top_n observations
        outfile: Path to file to write to
        top_n: Number of top elements to take from heap
    """
    n_largest = heapq.nlargest(top_n, heap)
    with open(outfile, 'w') as writer:
        for priority, node, data in n_largest:
            writer.write(data + "\n")
