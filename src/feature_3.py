"""
Feature 3

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from datetime import timedelta, datetime
import heapq
from typing import Dict, List, NewType, Optional, Tuple

from .pkg.common_methods import date_to_datetime


Deque = NewType("Deque", List[Tuple[datetime, str]])


def feature_3(queue: Deque,
              most_active_heap: List[Tuple[int, str]],
              parsed_line: Dict[str, str],
              top_n: int,
              time_rollover_queue: Deque,
              t_delta: timedelta=timedelta(minutes=60)):
    """
    List the top 10 busiest (or most frequently visited) 60-minute periods.

    For this challenge, we use two queues and a heap.
    Queue 1 (queue) contains all timestamps within t_delta time period.

    If we look at the first element of Queue 1 and notice that the new record
    has a timestamp greater than first element of Queue 1 + t_delta then we append that
    record to Queue 2 (time_rollover_queue), otherwise we keep appending to Queue 1.

    It is possible (and does occur) where all the minutes within a given hour form
    the top_n highest activity.

    If we have to append to Queue 2 then that means we have all values for the first
    element of Queue 1. We record the length of Queue 1 (all values within 60 minutes)
    and pop off the first value of Queue 1. We then append all values from time_rollover_heap
    that are within t_delta of the new first element of Queue 1.
    We then attempt to add the popped Queue 1 record to our heap if it belongs.

    Arguments:
        queue: Queue of all timestamps that fit into a given t_delta range
        most_active_heap: Store top_n active timestamps
        parsed_line: Dictionary of parsed log line
        top_n: Number of items to store in most_active_heap
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

        exhaust_queue(queue,
                      most_active_heap,
                      top_n,
                      time_rollover_queue)


def exhaust_queue(queue,
                  heap,
                  top_n,
                  time_rollover_queue,
                  t_delta: timedelta=timedelta(minutes=60)):
    """
    Record the length of the queue and pop off first element of queue.
    If there are consecutive elements in queue with the same timestamp
    as popped element then pop those as well.

    Pop elements from time_rollover_queue if elements in beginning of queue
    fit within the new first element of queue + t_delta and append them to queue

    Try to append the popped element and the recorded queue length
    to the heap which records the top_n 60 minute time windows.

    Arguments:
        queue: Queue of all timestamps that fit into a given t_delta range
        heap: Store top_n records
        top_n: Number of items to store in heap
        time_rollover_queue: Queue to store timestamps that don't fit into the t_delta
                             range and therefore cannot be appended to queue directly.
        t_delta: Time range to analyze
    """
    if not queue:
        return

    length_of_queue = len(queue)
    min_queue = queue.popleft()
    min_datetime_obj, min_timestamp_str = min_queue

    while queue and (queue[0][0] == min_datetime_obj):
        queue.popleft()

    while ((not queue and time_rollover_queue) or
           (time_rollover_queue and
            time_rollover_queue[0][0] <= queue[0][0] + t_delta)):
        rollover = time_rollover_queue.popleft()
        queue.append(rollover)

    if len(heap) < top_n:
        heapq.heappush(heap,
                       (length_of_queue,
                        min_timestamp_str))
    else:
        if length_of_queue > heap[0][0]:
            heapq.heappushpop(heap,
                              (length_of_queue,
                               min_timestamp_str))


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
        for priority, data in n_largest:
            writer.write(sep.join([data, str(priority)]) + "\n")
