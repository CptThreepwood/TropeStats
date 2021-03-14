import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
HTML_DIR = os.path.join(DATA_DIR, 'raw')
PARSED_DIR = os.path.join(DATA_DIR, 'parsed')
TROPE_INDEX_DIR = os.path.join(DATA_DIR, 'trope_index')

CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
TROPE_INDEX = os.path.join(CONFIG_DIR, 'all_tropes.yaml')
MEDIA_INDEX = os.path.join(CONFIG_DIR, 'all_media.yaml')
IGNORED_INDEX = os.path.join(CONFIG_DIR, 'ignored_namespaces.yaml')
