import os
import glob
import yaml
import time
import logging

from config import HTML_DIR, PARSED_DIR
from parsing.parse_html import get_links, is_ignored, article_from_url

logging.basicConfig(
    filename='logs/parse_html_{}.log'.format(time.time()),
    level=logging.DEBUG
)
articles = glob.glob(os.path.join(HTML_DIR, '*', '*.html'))
successes = 0
failures = 0
missing = 0
for article in articles:
    outname = os.path.splitext(article.replace(HTML_DIR, PARSED_DIR))[0] + '.yaml'
    if os.path.exists(outname) or is_ignored(article_from_url(article)):
        continue
    if not os.path.exists(os.path.dirname(outname)):
        os.makedirs(os.path.dirname(outname))
    print('Parsing {}'.format(article))
    bigraph_links = get_links(article)
    if any(link[0] == 'Err/Missing' for link in bigraph_links):
        failures += 1
        print('Failed')
        logging.error('Failed to parse {}'.format(article))
        for link in bigraph_links:
            if link[0] == 'Err/Missing':
                missing += 1
                logging.error('No such file {0}/{1}'.format(link[1].namespace, link[1].name))
    else:
        with open(outname, 'w') as out:
            print('Success:', outname)
            successes += 1
            yaml.dump(bigraph_links, out)

print('Successfully parsed {0} pages'.format(successes))
print('Missing {0} files required for {1} pages'.format(missing, failures))
