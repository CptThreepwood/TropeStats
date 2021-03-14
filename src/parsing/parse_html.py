import os
import bs4
import yaml

from typing import NamedTuple, List
from config import HTML_DIR, TROPE_INDEX, MEDIA_INDEX, IGNORED_INDEX

## -------------------------------------------------------------------------------------
## Article Type

class Article(NamedTuple):
    namespace: str
    name: str

    def to_string(self):
        return '/'.join([self.namespace, self.name])

def article_from_url(url: str) -> Article:
    path, _ = os.path.splitext(url)
    name = os.path.basename(path)
    namespace = os.path.basename(os.path.dirname(path))
    return Article(namespace, name)

## -------------------------------------------------------------------------------------
## Load Tropes

def get_trope_name(url: str) -> str:
    return os.path.basename(os.path.splitext(url)[0])

KNOWN_TROPES = [
    get_trope_name(url)
    for url in yaml.load(open(TROPE_INDEX), Loader=yaml.SafeLoader)
]

KNOWN_MEDIA = [
    name for name in yaml.load(open(MEDIA_INDEX), Loader=yaml.SafeLoader)
]

IGNORED_PAGES = [
    name for name in yaml.load(open(IGNORED_INDEX), Loader=yaml.SafeLoader)
]

## -------------------------------------------------------------------------------------
## Article Type Tests

def is_trope_namespace(article: Article) -> bool:
    return (article.namespace in KNOWN_TROPES)

def is_trope(article: Article) -> bool:
    return (article.name in KNOWN_TROPES) or is_trope_namespace(article)

def is_ignored(article: Article) -> bool:
    return any((page == article.name or page == article.namespace) for page in IGNORED_PAGES)

def is_media(article: Article) -> bool:
    return (article.namespace in KNOWN_MEDIA)

def is_subpage(linked_article: Article, article: Article) -> bool:
    '''
        Test if the linked article is a subpage of the given article
        Relies on the article not being named something generic in the namespace
        This is common in trope namespaces (e.g. ActionGirl/Literature)
        so we explicitly check for trope namespace
    '''
    return (
        linked_article.namespace == article.name
        and not is_trope_namespace(article)
        and not is_ignored(article)
    )

## -------------------------------------------------------------------------------------
## Article IO

def open_article(article: Article) -> str:
    article_name = os.path.join(HTML_DIR, article.namespace, article.name + '.html')
    with open(article_name, 'r', encoding='iso-8859-1') as article_io:
        return article_io.read()

## -------------------------------------------------------------------------------------
## Article Parsing

def get_internal_links(article: Article) -> List[Article]:
    soup = bs4.BeautifulSoup(open_article(article), features="html.parser")

    list_items = [
        item for item in soup.find_all('li')
        if len(item.find_all('a', class_='twikilink')) > 0
        and 'averted' not in str(item)
    ]
    return [
        # Incase this is a relative link. If it's absolute this shouldn't break anything
        article_from_url(os.path.join(article.namespace, link['href']))
        for trope in list_items
        for link in trope.find_all('a', class_='twikilink')
        if 'href' in link.attrs
    ]

def get_bigraph_links(article: Article) -> List[Article]:
    '''
        Returns the references to media if a trope page
        and the references to tropes on a media page.
        It should be smart enough to go to any subpages
    '''
    if not (is_ignored(article) or is_media(article) or is_trope(article)):
        raise TypeError('Unknown Page Type: ', article)
    try:
        internal_links = get_internal_links(article)

        subpages = [
            link for link in internal_links
            if is_subpage(link, article)
        ]
        refs = [
            link for link in internal_links
            if (not is_trope(article) and is_trope(link))
            or (is_trope(article) and not is_trope(link))
        ]

        for subpage in subpages:
            refs += get_bigraph_links(subpage)

        return { ref for ref in refs }
    except FileNotFoundError as err:
        return { Article('Err/Missing', article) }

def get_links(url: str) -> List[str]:
    return [article.to_string() for article in get_bigraph_links(article_from_url(url))]

if __name__ == '__main__':
    #article = Article('Main', 'ActionGirl')
    article = Article('OurDragonsAreDifferent', 'Literature') # Test namespace
    # article = Article('WesternAnimation', 'AvatarTheLastAirbender')
    try:
        test_tropes = get_bigraph_links(article)
        print(sorted(list(test_tropes)))
        print(len(test_tropes))
    except FileNotFoundError as err:
        print('Failed to parse {}'.format(article))
        print(err)
