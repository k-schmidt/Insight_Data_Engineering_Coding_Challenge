"""
Feature 4

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""
from datetime import datetime, timedelta
from typing import Dict, List, NewType

from common_methods import date_to_datetime

Deque = NewType("Deque", List[str])


def feature_4(parsed_line: Dict[str, str],
              user_dict: Dict[str, Deque],
              blocked_users: Dict[str, datetime],
              failed_login_td: timedelta=timedelta(seconds=20),
              blocked_td: timedelta=timedelta(minutes=5)):
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
            if len(user_dict[host]) == 3:
                blocked_users[host] = datetime_obj
                user_dict.pop(host)
        else:
            user_dict.pop(host, None)
