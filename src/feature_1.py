from typing import List, Tuple

from common_methods import append_to_heap
from trie import Node, Trie


def feature_1(host_trie: Trie,
              most_active_heap: List[Tuple[int, Node]],
              parsed_line: str,
              top_n: int) -> None:

    node = host_trie.add(parsed_line["host"])
    append_to_heap(node, most_active_heap, top_n)
