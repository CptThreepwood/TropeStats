import os
import io
import sys
import tomotopy

import time
import logging

from utils import get_matching_articles, load_parsed
from constants import PARSED_DIR, KNOWN_MEDIA

## Setup logging
def create_logger(name):
    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    file_handler = logging.FileHandler('logs/create_{}_model_{}.log'.format(name, time.time()))
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.addFilter(lambda record: record.levelno == logging.INFO)

    logger = logging.getLogger('{}_logger'.format(name))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_all_articles(pattern):
    articles = get_matching_articles(os.path.join(PARSED_DIR, pattern, '*.yaml'))
    return [
        [
            trope.trope_name()
            for trope in load_parsed(article)
            if trope.is_trope()
        ] for article in articles
    ]

def make_model():
    return tomotopy.HDPModel(
        ### Term weights
        tw=tomotopy.TermWeight.ONE,
        ## Minimum number of documents a term must appear in to not be ignored
        min_cf=3,
        ## Remove the top X most common terms
        rm_top=5,
        ## Concentration paramters ( I don't have an intution for these )
        # gamma=1, alpha=0.1,
        ## Initial guess at number of topics
        initial_k=10,
        ## Random seed, set for reproducible results
        seed=99999
    )

def train_model(article_pattern):
    logger = create_logger(article_pattern)
    docs = get_all_articles(article_pattern)

    model = make_model()
    for doc in docs:
        ## Sometimes a document has no links, and we ignore it
        if doc:
            model.add_doc(doc)

    model.burn_in = 100
    model.train(0)

    logger.info('Num docs: {}'.format(len(model.docs)))
    logger.info('Vocab size: {}'.format(len(model.used_vocabs)))
    logger.info('Num words: {}'.format(model.num_words))
    logger.info('Removed top words: {}'.format(model.removed_top_words))
    logger.info('Training...')

    for i in range(0, 100, 10):
        model.train(10)
        logger.info('Iteration: {}\tLog-likelihood: {}'.format(i, model.ll_per_word))

    with io.StringIO('') as io_buffer:
        model.summary(file=io_buffer)
        io_buffer.flush()
        summary = io_buffer.getvalue()
        logger.info(summary)
    if not os.path.exists('./models'):
        os.makedirs('./models')
    logger.info('Saving...')
    model.save('./models/{0}.hdp.bin'.format(article_pattern), True)

    important_topics = [k for k, v in sorted(enumerate(model.get_count_by_topics()), key=lambda x:x[1], reverse=True)]
    for k in important_topics:
        if not model.is_live_topic(k):
            continue
        logger.info('Topic #{}'.format(k))
        for word, prob in model.get_topic_words(k):
            logger.info('\t {} \t {}'.format(word, prob))

if __name__ == '__main__':
    for pattern in KNOWN_MEDIA:
        train_model(pattern)
    train_model('*')
