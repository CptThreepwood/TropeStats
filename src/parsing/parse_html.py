import os
import bs4
import yaml

from typing import NamedTuple, List
from utils import open_article, Article

## -------------------------------------------------------------------------------------
## Missing Local File Error

MISSING_SPACE = 'Err/Missing'

class MissingArticlesError(Exception):
    def __init__(self, articles):
        self.articles = articles

## -------------------------------------------------------------------------------------
## Article Parsing

def is_subpage(linked_article: Article, article: Article) -> bool:
    '''
        Test if the linked article is a subpage of the given article
        Relies on the article not being named something generic in the namespace
        This is common in trope namespaces (e.g. ActionGirl/Literature)
        so we explicitly check to see if we're already in a trope subpage (trope namespace)
    '''
    return (
        linked_article.namespace == article.name
        and not article.is_trope_namespace()
        and not article.is_ignored()
    )

def get_internal_links(article: Article) -> List[Article]:
    soup = bs4.BeautifulSoup(open_article(article), features="html.parser")

    list_items = [
        item for item in soup.find_all('li')
        if len(item.find_all('a', class_='twikilink')) > 0
        and 'averted' not in str(item)
    ]
    return [
        # Incase this is a relative link. If it's absolute this shouldn't break anything
        Article.from_url(os.path.join(article.namespace, link['href']))
        for trope in list_items
        for link in trope.find_all('a', class_='twikilink')
        if 'href' in link.attrs
    ]

def get_linked_articles(article: Article) -> List[Article]:
    '''
        Returns the references to media if a trope page
        and the references to tropes on a media page.
        It should be smart enough to go to any subpages
    '''
    try:
        internal_links = get_internal_links(article)

        subpages = [
            link for link in internal_links
            if is_subpage(link, article)
        ]
        for link in internal_links:
            print(link.to_string(), 'Trope' if link.is_trope() else 'Media')
        refs = [
            link for link in internal_links
            if (not article.is_trope() and link.is_trope())
            or (article.is_trope() and not link.is_trope())
        ]

        for subpage in subpages:
            refs += get_bigraph_links(subpage)

        return { ref for ref in refs }
    except FileNotFoundError as err:
        return { Article(MISSING_SPACE, article.to_string()) }

def get_links(url: str) -> List[str]:
    links = get_linked_articles(article_from_url(url))
    missing_files = [link.name for link in links if link.namespace == MISSING_SPACE]
    if len(missing_files) > 0:
        raise MissingArticlesError(missing_files)
    return [link.to_string() for link in links]

if __name__ == '__main__':
    # article = Article('Main', 'ActionGirl')
    # article = Article('OurDragonsAreDifferent', 'Literature') # Test namespace
    # article = Article('WesternAnimation', 'AvatarTheLastAirbender')
    article = Article('VideoGame', 'BaldursGate')
    try:
        test_tropes = get_linked_articles(article)
        print(sorted(list(test_tropes)))
        print(len(test_tropes))
    except FileNotFoundError as err:
        print('Failed to parse {}'.format(article))
        print(err)
