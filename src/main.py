from collections import deque
import heapq
import re

from common_methods import (gen_data_rows, parse_log_row)
from config import PATH_LOG_INPUT_FILE, regex_pattern
from feature_1 import feature_1
from feature_2 import feature_2
from feature_3 import feature_3
from trie import Trie


def main(log_file: str=PATH_LOG_INPUT_FILE, top_n: int=10):
    compiled_regex = re.compile(regex_pattern)
    host_trie = Trie()
    resource_trie = Trie()
    times_queue = deque()
    most_active_address_heap = []
    most_active_resource_heap = []
    most_active_time_heap = []

    for line in gen_data_rows(log_file):
        print(line)
        parsed_line = parse_log_row(line, compiled_regex)
        feature_1(host_trie,
                  most_active_address_heap,
                  parsed_line,
                  top_n)
        feature_2(resource_trie,
                  most_active_resource_heap,
                  parsed_line,
                  top_n)
        feature_3(times_queue,
                  most_active_time_heap,
                  parsed_line,
                  top_n)
    # print([(node.data, count) for count, node in heapq.nlargest(top_n, most_active_address_heap)])
    # print([(node.data, count) for count, node in heapq.nlargest(top_n, most_active_resource_heap)])
    print([(activity, timestamp_str) for activity, timestamp_str in heapq.nlargest(top_n, most_active_time_heap)])

if __name__ == '__main__':
    main()
