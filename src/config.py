"""
Configuration file for global variables
"""

import os

PATH_SRC = os.path.dirname(__file__)
PATH_ROOT = os.path.dirname(PATH_SRC)
PATH_LOG_INPUT = os.path.join(PATH_ROOT, "log_input")
PATH_LOG_INPUT_FILE = os.path.join(PATH_LOG_INPUT, "log.txt")

regex_pattern = r"(?P<host>(.*)) - - \[(?P<timestamp>(.*))\] \"(?P<request>(.*))\" (?P<http_reply_code>(\d{3})) (?P<bytes_transferred>(.*))"
