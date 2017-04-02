"""
Configuration file for global variables
"""

import os

PATH_SRC = os.path.dirname(__file__)
PATH_ROOT = os.path.dirname(PATH_SRC)
PATH_LOG_INPUT = os.path.join(PATH_ROOT, "log_input")
PATH_LOG_INPUT_FILE = os.path.join(PATH_LOG_INPUT, "log.txt")
PATH_LOG_OUTPUT = os.path.join(PATH_ROOT, "log_output")
PATH_ACTIVE_ADDRESSES = os.path.join(PATH_LOG_OUTPUT, "hosts.txt")
PATH_ACTIVE_RESOURCES = os.path.join(PATH_LOG_OUTPUT, "resources.txt")
PATH_ACTIVE_TIME = os.path.join(PATH_LOG_OUTPUT, "hours.txt")
PATH_BLOCKED_USER_LOG = os.path.join(PATH_LOG_OUTPUT, "blocked.txt")

regex_pattern = r"(?P<host>(.*)) - - \[(?P<timestamp>(.*))\] \"(?P<request>(.*))\" (?P<http_reply_code>(\d{3})) (?P<bytes_transferred>(.*))"
