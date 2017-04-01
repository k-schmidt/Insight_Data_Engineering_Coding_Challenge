import heapq
import re

from common_methods import gen_data_rows
from config import PATH_LOG_INPUT_FILE, regex_pattern
from trie import Trie


def feature_1(log_file: str=PATH_LOG_INPUT_FILE, top_x=10):
    host_trie = Trie()
    heap = []
    compiled_regex = re.compile(regex_pattern)

    for line in gen_data_rows(log_file):
        regex_object = re.search(compiled_regex, line)
        line_dict = regex_object.groupdict()
        node = host_trie.add(line_dict["host"])
        print(node.is_in_heap, heap)

        if len(heap) < top_x:
            if node.is_in_heap:
                for index, (count, heap_node) in enumerate(heap):
                    if node.data == heap_node.data:
                        heap[index] = (node.count, node)
                        heapq.heapify(heap)
                        break
            else:
                node.is_in_heap = True
                heapq.heappush(heap,
                               (node.count, node))
        else:
            if node.is_in_heap:
                for index, (count, heap_node) in enumerate(heap):
                    if node.data == heap_node.data:
                        heap[index] = (node.count, node)
                        heapq.heapify(heap)
                        break
            else:
                min_count_of_heap = heap[0][0]
                if node.count > min_count_of_heap:
                    node.is_in_heap = True
                    count, popped_node = heapq.heappushpop(heap,
                                                           (node.count, node))
                    popped_node.is_in_heap = False
    heapq.nlargest(top_x, heap)
    print([host for count, host in heap])

if __name__ == '__main__':
    print(feature_1())
