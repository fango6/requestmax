import bs4
import requests
from parsel import Selector
from requests.utils import guess_json_utf


class Extracter:
    """ embed Selector and BeautifulSoup. """

    @property
    def text(self):
        raise NotImplementedError

    @property
    def selector(self):
        if not hasattr(self, "_cached_selector"):
            self._cached_selector = Selector(text=self.text)
        return self._cached_selector

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query, **kwargs)

    def css(self, query):
        return self.selector.css(query)

    def re(self, regex, replace_entities=True):
        return self.selector.re(regex, replace_entities)

    def re_first(self, regex, default=None, replace_entities=True):
        return self.selector.re_first(regex, default, replace_entities)

    def soup(self, parser='html.parser'):
        if not hasattr(self, "_cached_soup"):
            self._cached_soup = bs4.BeautifulSoup(self.text, parser)
        return self._cached_soup

    def find(self, name=None, attrs={}, recursive=True, text=None, parser='html.parser', **kwargs):
        return self.soup(parser).find(name, attrs, recursive, text, **kwargs)

    def find_all(self, name=None, attrs={}, recursive=True, text=None, limit=None, parser='html.parser', **kwargs):
        return self.soup(parser).find_all(name, attrs, recursive, text, limit=limit, **kwargs)


class Response(requests.Response, Extracter):
    """ In order to embed Selector and BeautifulSoup """

    def _guess_encoding(self):
        if self.content and len(self.content) > 3:
            encoding = self.apparent_encoding
            if not encoding and not self.encoding:
                encoding = guess_json_utf(self.content)

            if encoding and self.encoding != encoding:
                self.encoding = encoding
        return self.encoding
