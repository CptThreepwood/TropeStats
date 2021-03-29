import glob
import yaml
from typing import List

from .Article import Article
from constants import *

## -------------------------------------------------------------------------------------
##

def get_matching_articles(pattern: str) -> List[Article]:
    return [
        Article.from_path(local_path)
        for local_path in glob.glob(pattern)
    ]

## -------------------------------------------------------------------------------------
## YAML IO

def load_parsed(article: Article) -> List[Article]:
    local_filename = os.path.join(PARSED_DIR, article.to_string() + '.yaml')
    with open(local_filename) as fio:
        return [
            Article.from_path(link)
            for link in yaml.load(fio, Loader=yaml.SafeLoader)
        ]

## -------------------------------------------------------------------------------------
## HTML IO

def open_article(article: Article) -> str:
    article_name = os.path.join(HTML_DIR, article.namespace, article.name + '.html')
    with open(article_name, 'r', encoding='iso-8859-1') as article_io:
        return article_io.read()

