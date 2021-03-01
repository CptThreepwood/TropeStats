import os
import bs4
import json
from constants import HTML_DIR, TROPE_INDEX

def get_trope_name(url):
    return url.split('/')[-1]

KNOWN_TROPES = [
    get_trope_name(url)
    for url in json.load(open(TROPE_INDEX))
]

def matches_trope(url):
    url_path_tokens = url.split('/')
    return any(
        (url_path_tokens[-1] == trope_name) or (url_path_tokens[-2] == trope_name)
        for trope_name in KNOWN_TROPES
    )

def matches_subpage(url, article):
    url_path_tokens = url.split('/')
    [media_type, media_name] = article.split('/')
    return media_name == url_path_tokens[-2]

def get_article_name(url):
    url_path_tokens = url.split('/')
    return '{}/{}'.format(url_path_tokens[-2], url_path_tokens[-1])

def open_article(article):
    article_name = os.path.join(HTML_DIR, article + '.html')
    with open(article_name, 'r', encoding='iso-8859-1') as article_io:
        return article_io.read()

def get_internal_links(html):
    soup = bs4.BeautifulSoup(html, features="html.parser")

    list_items = [
        item for item in soup.find_all('li')
        if len(item.find_all('a', class_='twikilink')) > 0
        and 'averted' not in str(item)
    ]
    return [
        link['href']
        for trope in list_items
        for link in trope.find_all('a', class_='twikilink')
        if 'href' in link.attrs
    ]

def get_bigraph_links(article):
    '''
        Returns the references to media if a trope page
        and the references to tropes on a media page.
        It should be smart enough to go to any subpages
    '''
    internal_links = get_internal_links(open_article(article))

    subpages = [
        get_article_name(link)
        for link in internal_links
        if matches_subpage(link, article)
    ]
    refs = [
        link
        for link in internal_links
        if (not matches_trope(article) and matches_trope(link))
        or (matches_trope(article) and not matches_trope(link))
    ]

    for subpage in subpages:
        refs += get_bigraph_links(subpage)

    return {
        os.path.basename(ref)
        for ref in refs
    }

if __name__ == '__main__':
    # article = 'Main/ActionGirl'
    article = 'WesternAnimation/AvatarTheLastAirbender'
    try:
        test_tropes = get_bigraph_links(article)
        print(sorted(list(test_tropes)))
        print(len(test_tropes))
    except FileNotFoundError as err:
        print('Failed to parse {}'.format(article))
        print(err)