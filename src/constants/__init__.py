import os
import yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
HTML_DIR = os.path.join(DATA_DIR, 'raw')
PARSED_DIR = os.path.join(DATA_DIR, 'parsed')
TROPE_INDEX_DIR = os.path.join(DATA_DIR, 'trope_index')

CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
TROPE_INDEX = os.path.join(CONFIG_DIR, 'all_tropes.yaml')
MEDIA_INDEX = os.path.join(CONFIG_DIR, 'all_media.yaml')
IGNORED_INDEX = os.path.join(CONFIG_DIR, 'ignored_namespaces.yaml')

## -------------------------------------------------------------------------------------
## Config IO

def load_config(filename):
    with open(filename) as fio:
        return yaml.load(fio, Loader=yaml.SafeLoader)

def load_tropes():
    return load_config(TROPE_INDEX)

def load_media():
    return load_config(MEDIA_INDEX)

def load_ignored():
    return load_config(IGNORED_INDEX)

## -------------------------------------------------------------------------------------
## Load Tropes

KNOWN_TROPES = load_tropes()
KNOWN_MEDIA = load_media()
IGNORED_PAGES = load_ignored()