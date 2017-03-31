from common_methods import gen_data_rows
from config import PATH_LOG_INPUT_FILE
from trie import Trie


def main(log_file: str=PATH_LOG_INPUT_FILE):
    for i, line in enumerate(gen_data_rows(log_file)):
        if i == 10:
            break
        print(line)

if __name__ == '__main__':
    print(main())
