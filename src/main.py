from collections import defaultdict, deque
import heapq
import re

from common_methods import (gen_data_rows,
                            parse_log_row,
                            write_top_n_heap_to_outfile)
from config import (PATH_LOG_INPUT_FILE,
                    regex_pattern,
                    PATH_ACTIVE_ADDRESSES,
                    PATH_ACTIVE_RESOURCES,
                    PATH_ACTIVE_TIME,
                    PATH_BLOCKED_USER_LOG)
from feature_1 import feature_1
from feature_2 import feature_2
from feature_3 import feature_3
from feature_4 import feature_4
from trie import Trie


def main(log_file: str=PATH_LOG_INPUT_FILE,
         most_active_addresses_outfile: str=PATH_ACTIVE_ADDRESSES,
         most_active_resources_outfile: str=PATH_ACTIVE_RESOURCES,
         most_active_time_outfile: str=PATH_ACTIVE_TIME,
         blocked_users_outfile: str=PATH_BLOCKED_USER_LOG,
         top_n: int=10):
    compiled_regex = re.compile(regex_pattern)
    host_trie = Trie()
    resource_trie = Trie()
    times_queue = deque()
    time_rollover_queue = deque()
    most_active_address_heap = []
    most_active_resource_heap = []
    most_active_time_heap = []
    max_hour_count = (None, None, None)
    user_dict = defaultdict(deque)
    blocked_users = dict()
    with open(blocked_users_outfile, 'w') as blocked_users_writer:

        for line in gen_data_rows(log_file):
            # print(line)
            parsed_line = parse_log_row(line, compiled_regex)
            feature_1(host_trie,
                      most_active_address_heap,
                      parsed_line,
                      top_n)
            feature_2(resource_trie,
                      most_active_resource_heap,
                      parsed_line,
                      top_n)
            max_hour_count = feature_3(times_queue,
                                       most_active_time_heap,
                                       parsed_line,
                                       top_n,
                                       max_hour_count,
                                       time_rollover_queue)
            if feature_4(parsed_line,
                         user_dict,
                         blocked_users):
                blocked_users_writer.write(line)

    write_top_n_heap_to_outfile(most_active_address_heap,
                                most_active_addresses_outfile,
                                top_n,
                                sep=",")
    write_top_n_heap_to_outfile(most_active_resource_heap,
                                most_active_resources_outfile,
                                top_n)
    write_top_n_heap_to_outfile(most_active_time_heap,
                                most_active_time_outfile,
                                top_n,
                                sep=",")

if __name__ == '__main__':
    main()
