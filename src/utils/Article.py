import os

from typing import NamedTuple
from constants import KNOWN_MEDIA, KNOWN_TROPES, IGNORED_PAGES

## -------------------------------------------------------------------------------------
## Article Type

class Article(NamedTuple):
    namespace: str
    name: str

    def from_url(url):
        '''
            Because we only care about the url after the domain, this is valid
            I could make this explicit with a URL parser, but it shouldn't matter
        '''
        return Article.from_path(url)
    
    def from_path(path):
        path, _ = os.path.splitext(path)
        name = os.path.basename(path)
        namespace = os.path.basename(os.path.dirname(path))
        return Article(namespace, name)

    def to_string(self):
        return '/'.join([self.namespace, self.name])

    def is_trope_namespace(self) -> bool:
        return (self.namespace in KNOWN_TROPES)

    def is_trope(self) -> bool:
        return (self.name in KNOWN_TROPES) or self.is_trope_namespace()

    def is_ignored(self) -> bool:
        return any((page == self.name or page == self.namespace) for page in IGNORED_PAGES)

    def is_media(self) -> bool:
        return (self.namespace in KNOWN_MEDIA)
