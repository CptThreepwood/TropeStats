import os
import sys
import glob
import yaml
import time
import logging

from config import HTML_DIR, PARSED_DIR
import parsing.parse_html as parse

## Setup logging
file_handler = logging.FileHandler('logs/parse_html_{}.log'.format(time.time()))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter('%(asctime)s - %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.addFilter(lambda record: record.levelno == logging.INFO)

logger = logging.getLogger('ParseAllLog')
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

## Find all the pages we've got downloaded
articles = glob.glob(os.path.join(HTML_DIR, '*', '*.html'))

successes = 0
failures = 0
missing = 0
for article in articles:
    outname = os.path.splitext(article.replace(HTML_DIR, PARSED_DIR))[0] + '.yaml'
    article_check = parse.article_from_url(article)

    ## Check if we know what this file should be
    if not (parse.is_ignored(article_check) or parse.is_media(article_check) or parse.is_trope(article_check)):
        logger.warning('Unknown Page Type: {0}'.format(article))
        continue

    ## Ignore pages we've already processed or we're deliberately ignoring
    if os.path.exists(outname) or parse.is_ignored(article_check):
        continue

    ## Create output dir if it doesn't exist
    if not os.path.exists(os.path.dirname(outname)):
        os.makedirs(os.path.dirname(outname))

    logger.info('Parsing {}'.format(article))
    try:
        bigraph_links = parse.get_links(article)
        with open(outname, 'w') as out:
            logger.info('Success {}'.format(outname))
            successes += 1
            yaml.dump(bigraph_links, out)
    except parse.MissingArticlesError as err:
        failures += 1
        logger.info('Failed')
        logger.error('Failed to parse {}'.format(article))
        missing += len(err.articles)
        for article in articles:
            logger.error('No such file {0}'.format(article))

logger.info('Successfully parsed {0} pages'.format(successes))
logger.info('Missing {0} files required for {1} pages'.format(missing, failures))
