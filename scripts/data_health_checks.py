import os
import glob

from constants import PARSED_DIR
from utils import get_matching_articles, load_parsed

def find_empty():
    parsed_data = get_matching_articles(os.path.join(PARSED_DIR, '*/*.yaml'))
    for p in parsed_data:
        if len(load_parsed(p)) == 0:
            print(p, 'contains no data')

if __name__ == '__main__':
    find_empty()