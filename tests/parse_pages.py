import os
import unittest

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from src.parsing import parse_html
parse_html.HTML_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

class TestParsing(unittest.TestCase):

    def test_media(self):
        '''
        Parsing a Media Page
        '''
        links = parse_html.get_links('Anime/AceAttorney')
        self.assertEqual(len(links), 174)

    def test_media_with_subpages(self):
        '''
        Parsing a Media Page with subpages
        '''
        links = parse_html.get_links('WesternAnimation/AvatarTheLastAirbender')
        self.assertEqual(len(links), 1337)

    def test_trope(self):
        '''
        Parsing a Media Page
        '''
        links = parse_html.get_links('Main/BadSanta')
        self.assertEqual(len(links), 305)

    def test_trope_with_subpages(self):
        '''
        Parsing a Trope Page with subpages
        '''
        links = parse_html.get_links('Main/ActionGirl')
        self.assertEqual(len(links), 1853)

if __name__ == '__main__':
    unittest.main()