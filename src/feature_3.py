"""
Feature 3

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from datetime import timedelta, datetime
import heapq
from typing import Dict, List, NewType, Tuple

from common_methods import date_to_datetime


Deque = NewType("Deque", Tuple[datetime, str])
def feature_3(queue: Deque,
              most_active_heap: List[Tuple[int, str]],
              parsed_line: Dict[str, str],
              top_n: int,
              t_delta: timedelta=timedelta(minutes=60)):
    log_timestamp = parsed_line["timestamp"]
    datetime_obj = date_to_datetime(log_timestamp)
    if not queue:
        queue.append((datetime_obj, log_timestamp))
        return

    min_queue_plus_timedelta = queue[0][0] + t_delta
    if datetime_obj <= min_queue_plus_timedelta:
        queue.append((datetime_obj, log_timestamp))

    else:
        length_of_queue = len(queue)
        min_queue = queue.popleft()
        min_datetime_obj, min_timestamp_str = min_queue

        while queue[0] == min_queue:
            queue.popleft()

        if len(most_active_heap) < top_n:
            heapq.heappush(most_active_heap,
                           (length_of_queue,
                            min_timestamp_str))
        else:
            if length_of_queue > most_active_heap[0][0]:
                heapq.heappushpop(most_active_heap,
                                  (length_of_queue,
                                   min_timestamp_str))
