"""
Common methods applicable to all problems.

Kyle Schmidt
Insight Data Engineering Coding Challenge
"""


def gen_data_rows(log_file: str):
    """
    Generate an infinite stream of data

    Arguments:
        log_file: (stream) path to data for analysis
    """
    with open(log_file, 'r', encoding="ISO-8859-1") as stream:
        for line in stream:
            yield line
