import os
import glob
import time
import requests

from config import ROOT_DIR, HTML_DIR

# ERROR:root:[Errno 2] No such file or directory: '/home/ubuntu/TropeStats/data/raw/BerserkButton/AnimeAndManga.html'

TVTROPES_BASE = 'http://tvtropes.org/pmwiki/pmwiki.php/'

def download_url(url, wait=2):
    try:
        return requests.get(url, timeout=10).content
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        print('timed out, retrying')
        time.sleep(wait)
        return download_url(url, wait*2)

def get_url(line):
    article = os.path.join(*line.split()[-1].strip("'").split('/')[-2:])
    return article, TVTROPES_BASE + os.path.splitext(article)[0]

def get_latest_log():
    logs = glob.glob(os.path.join(ROOT_DIR, 'logs', 'parse_html*.log'))
    return sorted(logs)[-1]

def download_and_store(line):
    article, url = get_url(line)
    outfile = os.path.join(HTML_DIR, os.path.splitext(article)[0] + '.html')
    if os.path.exists(outfile):
        return
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    print(outfile)
    with open(outfile, 'wb') as out_io:
        out_io.write(download_url(url))

if __name__ == '__main__':
    log_file = get_latest_log()
    with open(log_file, 'r') as log_io:
        for line in log_io.readlines():
            if 'No such file' in line:
                download_and_store(line)

