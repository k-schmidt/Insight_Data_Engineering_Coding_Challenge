"""
Common methods applicable to all problems.

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from datetime import datetime
import heapq
import re
from typing import Dict, Generator, List, Optional, Tuple

from trie import Node


def gen_data_rows(log_file: str) -> Generator[str, None, None]:
    """
    Generate an infinite stream of data

    Arguments:
        log_file: (stream) path to data for analysis

    Returns:
        Line of log file
    """
    with open(log_file, 'r', encoding="ISO-8859-1", errors="ignore") as stream:
        for line in stream:
            yield line


def parse_log_row(log_line: str, compiled_regex) -> Dict[str, str]:
    """
    Given a compiled regex pattern, parse log row for attributes

    Arguments:
        log_line: Row of log file
        compiled_regex: Regex compiled pattern

    Returns:
        Parsed log file
    """
    regex_object = re.search(compiled_regex, log_line)
    try:
        line_dict = regex_object.groupdict()
    except AttributeError:
        raise AttributeError
    return line_dict


def is_valid_crud(request: str) -> bool:
    """
    Check if the request string contains a valid CRUD operation
    in order to determine if the request can be considered for evaluation

    Arguments:
        request: Request string from log file
            (Usually) takes the form of:
                "GET /images/KSC-logosmall.gif HTTP/1.0"
    Returns:
        Boolean if request is valid or not
    """
    valid_crud = {"GET", "POST", "PATCH", "PUT", "DELETE"}
    beginning_of_request = request[:6]  # We don't need to check entire request
    if len(list(filter(lambda x: x in beginning_of_request, valid_crud))) == 1:
        return True
    return False


def format_bytes(parsed_line: Dict[str, str]) -> int:
    """
    Parse transferred bytes and cast them to integers

    Arguments:
        parsed_line: Dictionary of the parsed log file after regex

    Returns:
        Bytes as integer
    """
    transferred_bytes = parsed_line["bytes_transferred"]
    if transferred_bytes == "-":
        return 0
    return int(transferred_bytes)


def append_to_heap(node: Node,
                   heap: List[Tuple[int, Node]],
                   top_n: int):
    """
    Given a node and a heap, fill the heap until it is
    of length top_n. While initially filling heap,
    if node is in the heap then we will want to update its count
    and reorder the heap. Otherwise, we will append until the heap
    is of length top_n.

    Once heap is of length top_n, we will again want to check if the
    node is already in the heap and update its count and reorder the heap.
    Otherwise, we will append to heap if we discover a node that is greater than
    the minimum node in the heap.

    Arguments:
        node: Node in Trie that contains all of its representative data
        heap: Heap to maintain top_n node priorities
        top_n: length of heap
    """
    if len(heap) < top_n:
        if node.is_in_heap:
            for index, (count, heap_node) in enumerate(heap):
                if node.data == heap_node.data:
                    heap[index] = (node.count, node)
                    heapq.heapify(heap)
                    break
        else:
            node.is_in_heap = True
            heapq.heappush(heap, (node.count, node))
    else:
        if node.is_in_heap:
            for index, (count, heap_node) in enumerate(heap):
                if node.data == heap_node.data:
                    heap[index] = (node.count, node)
                    heapq.heapify(heap)
                    break
        else:
            min_count_in_heap = heap[0][0]
            if node.count > min_count_in_heap:
                node.is_in_heap = True
                count, popped_node = heapq.heappushpop(heap,
                                                       (node.count, node))
                popped_node.is_in_heap = False


def date_to_datetime(timestamp_str: str,
                     timestamp_pattern: str="%d/%b/%Y:%H:%M:%S -0400") -> datetime:
    """
    Create datetime object from given timestamp string

    Arguments:
        timestamp_str: Timestamp string
        timestamp_pattern: Format of timestamp to expect
            default: %d/%b/%Y:%H:%M:%S -0400

    Returns:
        Python datetime object
    """
    datetime_obj = datetime.strptime(timestamp_str, timestamp_pattern)
    return datetime_obj


def write_top_n_heap_to_outfile(heap,
                                outfile,
                                top_n,
                                sep: Optional[str]=None):
    """
    Given a heap in the format of (priority, data),
    sort the heap in decreasing order.

    This function is specific to features 1-3

    Side Effect: Write to outfile
    """
    n_largest = heapq.nlargest(top_n, heap)
    with open(outfile, 'w') as writer:
        if sep:
            for priority, data in n_largest:
                if isinstance(data, Node):  # logic for feature 1
                    writer.write(sep.join([data.data, str(priority)]) + "\n")
                else:  # logic for feature 3
                    writer.write(sep.join([data, str(priority)]) + "\n")
        else:
            for _, node in n_largest:  # logic for feature 2
                writer.write(node.data + "\n")
