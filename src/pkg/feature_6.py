"""
Feature 6

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from datetime import datetime
from typing import Dict

from .common_methods import date_to_datetime


def add_hour_to_dict(common_times: Dict[str, int],
                     parsed_line: Dict[str, str]) -> None:
    """
    Count the number of views for each hour

    Arguments:
        common_times: Dictionary of Hours to their counts
        parsed_line: Dictionary of parsed log file
    """
    log_timestamp = parsed_line["timestamp"]
    try:
        datetime_obj = date_to_datetime(log_timestamp)
    except ValueError:
        return

    hour_string = format_hour_str(datetime_obj)

    common_times[hour_string] += 1


def format_hour_str(datetime_obj: datetime):
    """
    Convert Hour to String Format H:M:S

    Arguments:
        datetime_obj: Datetime object to format

    Returns:
        String formated time
    """
    return datetime.strptime(
        str(datetime_obj.hour),
        "%H").strftime("%H:%M:%S")
