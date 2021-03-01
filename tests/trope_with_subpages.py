import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
# from scraping import constants, get_links
import scraping.parse_media_for_tropes

scraping.parse_media_for_tropes.HTML_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
links = scraping.parse_media_for_tropes.get_links('Main/ActionGirl')
print(links)
print(len(links))