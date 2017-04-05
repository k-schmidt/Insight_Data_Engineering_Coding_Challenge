"""
Feature 5

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from datetime import datetime, timedelta
import heapq
from typing import Dict, List, NewType, Optional, Tuple

from .common_methods import date_to_datetime


Deque = NewType("Deque", List[Tuple[datetime, str]])


def feature_5(queue: Deque,
              heap: List[Tuple[int, str]],
              parsed_line: Dict[str, str],
              top_n: int,
              max_hour_count: Tuple[Optional[datetime], Optional[str], Optional[int]],
              time_rollover_queue: Deque,
              t_delta: timedelta=timedelta(minutes=60)):
    """
    List the top 10 busiest (or most frequently visited) 60-minute periods,
    non-consecutive.

    For this challenge, we use two queues and a heap.
    Queue 1 (queue) contains all timestamps within t_delta time period.

    If we look at the first element of Queue 1 and notice that the new record
    has a timestamp greater than first element of Queue 1 + t_delta then we append that
    record to Queue 2 (time_rollover_queue), otherwise we keep appending to Queue 1.

    It is possible (and does occur) where all the minutes within a given hour form
    the top_n highest activity.

    Therefore, we keep a max for that hour called max_hour_count that holds the max length
    of Queue 1 for that hour until we reach the end of that 60 minute interval.

    If we have to append to Queue 2 then that means we have all values for the first
    element of Queue 1. We record the length of Queue 1 (all values within 60 minutes)
    and pop off the first value of Queue 1. We then append all values from time_rollover_heap
    that are within t_delta of the new first element of Queue 1.
    We then attempt to add the popped Queue 1 record to our heap if it belongs.

    Arguments:
        queue: Queue of all timestamps that fit into a given t_delta range
        heap: Store top_n active timestamps
        parsed_line: Dictionary of parsed log line
        top_n: Number of items to store in most_active_heap
        max_hour_count: Variable to store the max information over the past t_delta time period.
        time_rollover_queue: Queue to store timestamps that don't fit into the t_delta
                             range and therefore cannot be appended to queue directly.
        t_delta: Time range to analyze
    """
    log_timestamp = parsed_line["timestamp"]
    try:
        datetime_obj = date_to_datetime(log_timestamp)
    except ValueError:
        return
    if not queue:
        queue.append((datetime_obj, log_timestamp))
        return

    min_queue_plus_timedelta = queue[0][0] + t_delta
    if datetime_obj <= min_queue_plus_timedelta:
        queue.append((datetime_obj, log_timestamp))

    else:
        time_rollover_queue.append((datetime_obj, log_timestamp))
        length_of_queue = len(queue)
        min_queue = queue.popleft()
        min_datetime_obj, min_timestamp_str = min_queue

        while queue and (queue[0][0] == min_datetime_obj):
            queue.popleft()

        while not queue or (time_rollover_queue and
                            time_rollover_queue[0][0] <= queue[0][0] + t_delta):
            rollover = time_rollover_queue.popleft()
            queue.append(rollover)

        if not max_hour_count:
            max_hour_count = (min_datetime_obj,
                              min_timestamp_str,
                              length_of_queue)
        else:
            max_time_obj, max_timestamp_str, frequency = max_hour_count
            if (min_datetime_obj <= max_time_obj + t_delta and
                length_of_queue > frequency):
                max_hour_count = (min_datetime_obj,
                                  min_timestamp_str,
                                  length_of_queue)
            elif (min_datetime_obj > max_time_obj + t_delta):
                if len(heap) < top_n:
                    heapq.heappush(heap,
                                   (frequency,
                                    max_timestamp_str))
                else:
                    if frequency > heap[0][0]:
                        heapq.heappushpop(heap,
                                          (frequency,
                                           max_timestamp_str))

                max_hour_count = (min_datetime_obj,
                                  min_timestamp_str,
                                  length_of_queue)
    return max_hour_count
