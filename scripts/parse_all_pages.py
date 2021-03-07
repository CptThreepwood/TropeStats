import os
import glob
import json
import time
import logging

from config import HTML_DIR, PARSED_DIR
from parsing.parse_html import get_links

logging.basicConfig(
    filename='logs/parse_html_{}.log'.format(time.time()),
    level=logging.DEBUG
)
articles = glob.glob(os.path.join(HTML_DIR, '*', '*.html'))
for article in articles:
    outname = os.path.splitext(article.replace(HTML_DIR, PARSED_DIR))[0] + '.json'
    if os.path.exists(outname):
        continue
    if not os.path.exists(os.path.dirname(outname)):
        os.makedirs(os.path.dirname(outname))
    try:
        print(outname)
        bigraph_links = get_links(article)
        with open(outname, 'w') as out:
            json.dump(bigraph_links, out)
    except FileNotFoundError as err:
        logging.error('Failed to parse {}'.format(article))
        logging.error(err)
