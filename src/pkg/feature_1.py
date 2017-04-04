"""
Feature 1

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import heapq
from typing import List, Tuple

from .common_methods import append_to_heap
from .trie import Node, Trie


def feature_1(host_trie: Trie,
              most_active_heap: List[Tuple[int, Node]],
              parsed_line: str,
              top_n: int) -> None:
    """
    Identify the top 10 most active IP/host addresses
    that have accessed the website.

    We append the host/IP addresses to a Trie
    and within the last node of the Trie for that host/IP address
    we keep track of the host/IP address frequency count and whether it is in the heap.
    We maintain a heap for easy access to the minumum element of the top_n
    host/IP addresses.

    If the nodes is in the heap then we do a linear traversal to find it
    and update its priority.

    Otherwise we append the node to the heap and pop the minimum element of the heap
    if the heap is greater than top_n.

    Arguments:
        host_trie: Trie to hold each character that makes up a host/IP address
        most_active_heap: Heap to store top_n host/IP addresses
        parsed_line: Dictionary of parsed log line
        top_n: Number of items to store in most_active_heap
    """
    node, item = host_trie.add(parsed_line["host"])
    append_to_heap(node, item, most_active_heap, top_n)


def write_top_n_heap_to_outfile(heap,
                                outfile,
                                top_n,
                                sep=","):
    """
    Write top_n of heap to outfile, comma separated
    values of the item in the heap and its priority

    Arguments:
        heap: Heap of top_n observations
        outfile: Path to file to write to
        top_n: Number of top elements to take from heap
        sep: File delimiter
    """
    n_largest = heapq.nlargest(top_n, heap)
    with open(outfile, 'w') as writer:
        for priority, node, item in n_largest:
            writer.write(sep.join([item, str(priority)]) + "\n")
