import os
import bs4
import json

ARTICLE_PATH = './raw/pmwiki.php'
SCRIPT_PATH = os.path.dirname(__file__)

def get_trope_name(url):
    return url.split('/')[-1]

KNOWN_TROPES = [
    get_trope_name(url)
    for url in json.load(open(os.path.join(SCRIPT_PATH, 'trope_index', 'all_tropes.json')))
]

def matches_trope(url):
    url_path_tokens = url.split('/')
    return any(
        (url_path_tokens[-1] == trope_name) or (url_path_tokens[-2] == trope_name)
        for trope_name in KNOWN_TROPES
    )

def open_article(article):
    article_name = os.path.join(ARTICLE_PATH, article + '.html')
    print(article_name)
    with open(article_name, 'r', encoding='iso-8859-1') as article_io:
        return article_io.read()

def get_tropes_in_article(article):
    soup = bs4.BeautifulSoup(open_article(article), features="html.parser")

    tropes = [
        item for item in soup.find_all('li')
        if len(item.find_all('a', class_='twikilink')) > 0
        and 'averted' not in str(item)
    ]
    refs = [
        link['href']
        for trope in tropes
        for link in trope.find_all('a', class_='twikilink')
        if 'href' in link.attrs
        if matches_trope(link['href'])
    ]
    return {
        os.path.basename(ref)
        for ref in refs
    }

if __name__ == '__main__':
    test_tropes = get_tropes_in_article('Anime/AceAttorney')
    print(sorted(list(test_tropes)))
    print(len(test_tropes))