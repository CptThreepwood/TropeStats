import os
import bs4
import json
import time
import requests

from ..config import TROPE_INDEX, TROPE_INDEX_DIR

TROPE_LIST_BASE = "https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope"

def get_trope_list_page(n=1):
    response = requests.get('{}&page={}'.format(TROPE_LIST_BASE, n))
    return response.content

def parse_tropes(content):
    soup = bs4.BeautifulSoup(content, features="html.parser")
    return [
        link['href']
        for link in soup.find(id='main-article').find('table').find_all('a')
    ]

def save_trope_page(content, i):
    with open(os.path.join(TROPE_INDEX_DIR, 'page_{}.html'.format(i)), 'wb') as html_io:
        html_io.write(content)

if __name__ == '__main__':
    i = 1
    tropes = []
    content = get_trope_list_page(i)
    new_tropes = parse_tropes(content)
    while len(new_tropes) > 0:
        save_trope_page(content, i)
        tropes += new_tropes
        i += 1
        time.sleep(1)
        content = get_trope_list_page(i)
        new_tropes = parse_tropes(content)
    with open(TROPE_INDEX, 'w') as f:
        json.dump(tropes, f)
