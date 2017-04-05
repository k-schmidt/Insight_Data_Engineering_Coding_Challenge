"""
Main module

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from collections import defaultdict, deque
import heapq
import re
from typing import Dict, List, Tuple

from config import (PATH_LOG_INPUT_FILE,
                    regex_pattern,
                    PATH_ACTIVE_ADDRESSES,
                    PATH_ACTIVE_RESOURCES,
                    PATH_ACTIVE_TIME,
                    PATH_BLOCKED_USER_LOG,
                    PATH_NON_CONSECUTIVE_TIME,
                    PATH_POPULAR_TIMES,
                    PATH_POPULAR_DAYS)
from pkg.feature_1 import feature_1, write_top_n_heap_to_outfile as write_feature_1
from pkg.feature_2 import feature_2, write_top_n_heap_to_outfile as write_feature_2
from pkg.feature_3 import feature_3, exhaust_queue, write_top_n_heap_to_outfile as write_feature
from pkg.feature_4 import feature_4
from pkg.feature_5 import feature_5
from pkg.feature_6 import add_hour_to_dict
from pkg.feature_7 import add_day_count_to_dict
from pkg.common_methods import (gen_data_rows,
                                parse_log_row,
                                write_additional_feature)
from pkg.trie import Node, Trie


def write_features(address_heap: List[Tuple[int, Node, str]],
                   address_outfile: str,
                   resource_heap: List[Tuple[int, Node, str]],
                   resource_outfile: str,
                   time_heap: List[Tuple[int, Node, str]],
                   time_outfile: str,
                   non_consecutive_time_heap: List[Tuple[int, Node, str]],
                   non_consecutive_time_outfile: str,
                   popular_times: Dict[str, int],
                   popular_times_outfile: str,
                   popular_days: Dict[str, int],
                   popular_days_outfile: str,
                   top_n: int) -> None:
    """
    Write top_n of heaps to file

    Arguments:
        address_heap: Top host/IP Addresses in a heap
        address_outfile: Path to write top addresses
        resource_heap: Top resources in a heap
        resource_outfile: Path to write top resources
        time_heap: Top times in a heap
        time_outfile: Path to write top times
        top_n: Number of items from heap to extract
    """
    write_feature_1(address_heap,
                    address_outfile,
                    top_n)
    write_feature_2(resource_heap,
                    resource_outfile,
                    top_n)
    write_feature(time_heap,
                  time_outfile,
                  top_n)
    write_feature(non_consecutive_time_heap,
                  non_consecutive_time_outfile,
                  top_n)
    write_additional_feature(popular_times,
                             popular_times_outfile)
    write_additional_feature(popular_days,
                             popular_days_outfile)


def main(log_file: str=PATH_LOG_INPUT_FILE,
         most_active_addresses_outfile: str=PATH_ACTIVE_ADDRESSES,
         most_active_resources_outfile: str=PATH_ACTIVE_RESOURCES,
         most_active_time_outfile: str=PATH_ACTIVE_TIME,
         blocked_users_outfile: str=PATH_BLOCKED_USER_LOG,
         non_consecutive_time_outfile: str=PATH_NON_CONSECUTIVE_TIME,
         popular_times_outfile: str=PATH_POPULAR_TIMES,
         popular_days_outfile: str=PATH_POPULAR_DAYS,
         top_n: int=10):
    compiled_regex = re.compile(regex_pattern)
    host_trie = Trie()
    resource_trie = Trie()
    times_queue = deque()
    time_rollover_queue = deque()
    most_active_address_heap = []
    most_active_resource_heap = []
    most_active_time_heap = []
    user_dict = defaultdict(deque)
    blocked_users = dict()
    max_hour_count = (None, None, None)
    non_consecutive_time_heap = []
    non_consecutive_rollover_queue = deque()
    non_consecutive_time_queue = deque()
    popular_times = defaultdict(int)
    popular_days = defaultdict(int)

    with open(blocked_users_outfile, 'w') as blocked_users_writer:

        for line in gen_data_rows(log_file):
            try:
                parsed_line = parse_log_row(line, compiled_regex)
            except AttributeError:
                continue
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
                      top_n,
                      time_rollover_queue)
            if feature_4(parsed_line,
                         user_dict,
                         blocked_users):
                blocked_users_writer.write(line)
            max_hour_count = feature_5(non_consecutive_time_queue,
                                       non_consecutive_time_heap,
                                       parsed_line,
                                       top_n,
                                       max_hour_count,
                                       non_consecutive_rollover_queue)
            add_hour_to_dict(popular_times,
                             parsed_line)
            add_day_count_to_dict(popular_days,
                                  parsed_line)

    while times_queue:
        exhaust_queue(times_queue,
                      most_active_time_heap,
                      top_n,
                      time_rollover_queue)

    write_features(most_active_address_heap,
                   most_active_addresses_outfile,
                   most_active_resource_heap,
                   most_active_resources_outfile,
                   most_active_time_heap,
                   most_active_time_outfile,
                   non_consecutive_time_heap,
                   non_consecutive_time_outfile,
                   popular_times,
                   popular_times_outfile,
                   popular_days,
                   popular_days_outfile,
                   top_n)

if __name__ == '__main__':
    main()
