"""
Feature 4

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from datetime import datetime, timedelta
from typing import Dict, List, NewType

from .common_methods import date_to_datetime

Deque = NewType("Deque", List[str])


def feature_4(parsed_line: Dict[str, str],
              user_dict: Dict[str, Deque],
              blocked_users: Dict[str, datetime],
              failed_login_td: timedelta=timedelta(seconds=20),
              blocked_td: timedelta=timedelta(minutes=5),
              consecutive_failed_logins: int=3):
    """
    Detect patterns of three failed login attempts from the same IP address
    over 20 seconds so that all further attempts to the site can be blocked
    for 5 minutes. Log those possible security breaches

    For this challenge we use two dictionaries.
    blocked_users: Dictionary maps a host to a timestamp
    user_dict: Dictionary maps a host to consecutive failed login attempts
               held in queue

    If an observed host is in the blocked user dictionary and the observed
    timestamp is less than blocked_td, then we will log that as a security breach.

    If an observed host is in the blocked user dictionary and the observed
    timstamp is greater than blocked_td, then we will remove the host from blocked_user.
    If the observed http status code is 401 (signifying a failed login attemp) then
    we will append the observed host and that timestamp to the user_dict.

    If the observed host is not in the blocked user dictionary and the
    observed http status code is 401 then we will first remove
    all timestamps of that host that are less than observed timestamp - failed_login_td
    and append the observed timestamp.

    If the length of the queue for that observed host within user_dict becomes 3
    then we will put the observed host and timestamp in the blocked_users dictionary
    and remove the observed host from the user_dict.

    Arguments:
        parsed_line: Dictionary of parsed log line
        user_dict: Represents a users consecutive failed login attempts
                   within failed_login_td
        blocked_users: Users who are blocked for blocked_td length of time
        failed_login_td: Length of time to monitor for failed login attempts
        blocked_td: Length of time a host should stay in blocked_users
    """
    http_status_code = parsed_line["http_reply_code"]
    log_timestamp = parsed_line["timestamp"]
    datetime_obj = date_to_datetime(log_timestamp)
    host = parsed_line["host"]
    if (host in blocked_users and
        datetime_obj <= blocked_users[host] + blocked_td):
        return True  # log user

    elif (host in blocked_users and
          datetime_obj > blocked_users[host] + blocked_td):
        blocked_users.pop(host)

        if http_status_code == "401":
            user_dict[host].append(datetime_obj)

    else:
        if http_status_code == "401":
            while (user_dict[host] and
                   user_dict[host][0] + failed_login_td < datetime_obj):
                user_dict[host].popleft()

            user_dict[host].append(datetime_obj)
            if len(user_dict[host]) == consecutive_failed_logins:
                blocked_users[host] = datetime_obj
                user_dict.pop(host)
        else:
            user_dict.pop(host, None)
