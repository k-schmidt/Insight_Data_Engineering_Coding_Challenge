"""
Feature 7

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
import calendar
from datetime import datetime, date
from typing import Dict

from .common_methods import date_to_datetime


def datetime_obj_to_weekday_name(datetime_obj: datetime) -> str:
    """
    Get string name for weekday integer

    Arguments:
        datetime_obj: Datetime object representation of the timestamp

    Returns:
        String weekday
    """
    return calendar.day_name[datetime_obj.date().weekday()]


def add_day_count_to_dict(popular_days: Dict[int, int],
                          parsed_line: Dict[str, str]) -> None:
    """
    Increment counts for each observed weekday

    Arguments:
        popular_days: Dictionary of Day strings to their counts
        parsed_line: Dictionary representation of the parsed log row
    """
    log_timestamp = parsed_line["timestamp"]
    try:
        datetime_obj = date_to_datetime(log_timestamp)
    except ValueError:
        return

    weekday_str = datetime_obj_to_weekday_name(datetime_obj)
    popular_days[weekday_str] += 1
