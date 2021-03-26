import yaml

from .Article import Article
from constants import *

## -------------------------------------------------------------------------------------
## YAML IO

def load_parsed(article):
    local_filename = os.path.join(PARSED_DIR, article.to_string() + '.yaml')
    with open(local_filename) as fio:
        return yaml.load(fio, Loader=yaml.SafeLoader)

## -------------------------------------------------------------------------------------
## HTML IO

def open_article(article: Article) -> str:
    article_name = os.path.join(HTML_DIR, article.namespace, article.name + '.html')
    with open(article_name, 'r', encoding='iso-8859-1') as article_io:
        return article_io.read()

