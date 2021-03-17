import os
import glob
import time
import requests

from config import ROOT_DIR, HTML_DIR

TVTROPES_BASE = 'http://tvtropes.org/pmwiki/pmwiki.php/'

def download_url(url, wait=2):
    try:
        return requests.get(url, timeout=10).content
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        print('timed out, retrying')
        time.sleep(wait)
        return download_url(url, wait*2)

def get_url(article):
    return os.path.join(TVTROPES_BASE, article.to_string())

def download_and_store(article):
    url = get_url(article)
    outfile = os.path.join(HTML_DIR, article.to_string())
    if os.path.exists(outfile):
        return
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    with open(outfile, 'wb') as out_io:
        out_io.write(download_url(url))