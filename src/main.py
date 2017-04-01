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
        print(line)
        regex_object = re.search(compiled_regex, line)
        line_dict = regex_object.groupdict()
        print(line_dict)
        node = host_trie.add(line_dict["host"])

        if len(heap) < top_x:
            for index, (count, host) in enumerate(heap):
                if node.data == host:
                    heap[index] = (node.count, node.data)
                    heapq.heapify(heap)
                    break
            else:
                heapq.heappush(heap, (node.count, node.data))
        else:
            for index, (count, host) in enumerate(heap):
                if node.data == host:
                    heap[index] = (node.count, node.data)
                    heapq.heapify(heap)
                    break
            else:
                min_count_of_heap = heap[0][0]
                if node.count > min_count_of_heap:
                    heapq.heappushpop(heap, (node.count, node.data))
    print(heapq.nlargest(top_x, heap))

if __name__ == '__main__':
    print(feature_1())
