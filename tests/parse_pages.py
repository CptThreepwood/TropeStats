import os
import unittest

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import parsing.parse_html
parsing.parse_html.HTML_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestParsing(unittest.TestCase):

    def test_media(self):
        '''
        Parsing a Media Page
        '''
        links = scraping.parse_media_for_tropes.get_links('Anime/AceAttorney')
        self.assertEqual(len(links), 174)

    def test_media_with_subpages(self):
        '''
        Parsing a Media Page with subpages
        '''
        links = scraping.parse_media_for_tropes.get_links('WesternAnimation/AvatarTheLastAirbender')
        self.assertEqual(len(links), 1337)

    def test_trope(self):
        '''
        Parsing a Media Page
        '''
        links = scraping.parse_media_for_tropes.get_links('Main/BadSanta')
        self.assertEqual(len(links), 305)

    def test_trope_with_subpages(self):
        '''
        Parsing a Trope Page with subpages
        '''
        links = scraping.parse_media_for_tropes.get_links('Main/ActionGirl')
        self.assertEqual(len(links), 1853)

# print(links)
# print(len(links))

# scraping.parse_media_for_tropes.HTML_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
# passed = len(links) == 
# print('Trope page with subpages: {}'.format('passed' if passed else 'failed'))
# print(links)
# print(len(links))

if __name__ == '__main__':
    unittest.main()