"""
Configuration file for global variables

Kyle Schmidt
Insight Data Engineering Coding Challenge
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
PATH_POPULAR_TIMES = os.path.join(PATH_LOG_OUTPUT, "popular_times.txt")
PATH_POPULAR_DAYS = os.path.join(PATH_LOG_OUTPUT, "popular_days.txt")
PATH_NON_CONSECUTIVE_TIME = os.path.join(PATH_LOG_OUTPUT, "non_consecutive.txt")
PATH_LOG_TEST_FILE = os.path.join(PATH_ROOT,
                                  "insight_testsuite",
                                  "tests",
                                  "test_features",
                                  "log_input",
                                  "log.txt")

PATH_TEST_DIR = os.path.join(PATH_ROOT, "tests")
PATH_TEST_DATA_DIR = os.path.join(PATH_TEST_DIR, "test_data")
PATH_TEST_DATA = os.path.join(PATH_TEST_DATA_DIR, "test.txt")
PATH_TEST_ACTIVE_ADDRESSES = os.path.join(PATH_TEST_DATA_DIR, "hosts.txt")
PATH_TEST_ACTIVE_RESOURCES = os.path.join(PATH_TEST_DATA_DIR, "resources.txt")
PATH_TEST_ACTIVE_TIME = os.path.join(PATH_TEST_DATA_DIR, "hours.txt")
PATH_TEST_ADDL_FEATURE_EXPORT = os.path.join(PATH_TEST_DIR, "additional_features.txt")

regex_pattern = r"(?P<host>(.*)) - - \[(?P<timestamp>(.*))\] (\“|\")(?P<request>(.*))(\“|\") (?P<http_reply_code>(\d{3})) (?P<bytes_transferred>(.*))"
