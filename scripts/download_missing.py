import os
import glob
import time
import requests

from config import ROOT_DIR, HTML_DIR
from scraping.downloader import download_and_store
import parsing.parse_html as parse

# ERROR:root:[Errno 2] No such file or directory: '/home/ubuntu/TropeStats/data/raw/BerserkButton/AnimeAndManga.html'

def get_article(line):
    return parse.article_from_url(line.split()[-1])

def get_latest_log():
    logs = glob.glob(os.path.join(ROOT_DIR, 'logs', 'parse_html*.log'))
    return sorted(logs)[-1]

if __name__ == '__main__':
    log_file = get_latest_log()
    with open(log_file, 'r') as log_io:
        for line in log_io.readlines():
            if 'No such file' in line:
                download_and_store(line)
