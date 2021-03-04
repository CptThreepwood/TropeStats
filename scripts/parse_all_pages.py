import os
import glob
import json
from config import HTML_DIR, PARSED_DIR
from parsing.parse_html import get_links

articles = glob.glob(os.path.join(HTML_DIR, '*', '*.html'))
for article in articles:
    try:
        bigraph_links = get_links(article)
        outname = os.path.splitext(article.replace(HTML_DIR, PARSED_DIR)) + '.json'
        with open(outname, 'w') as out:
            json.dump(bigraph_links, out)
    except FileNotFoundError as err:
        print('Failed to parse {}'.format(article))
        print(err)