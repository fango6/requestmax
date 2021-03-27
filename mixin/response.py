import re

import bs4
import requests
import six
from parsel import Selector as ParselSelector
from parsel.utils import extract_regex as parsel_extract_regex
from requests.utils import guess_json_utf


def extract_regex(regex, text, replace_entities=True):
    if isinstance(regex, six.string_types):
        # "." matches any character at all, including the newline.
        regex = re.compile(regex, re.UNICODE | re.DOTALL)
    return parsel_extract_regex(regex, text, replace_entities)


class Selector(ParselSelector):

    def re(self, regex, replace_entities=True):
        return extract_regex(regex, self.get(), replace_entities=replace_entities)


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

    def _revise_encoding(self):
        """ 检查并修正部分的编码不正确问题 """
        if self.content and len(self.content) > 3:
            encoding = self.apparent_encoding
            if not encoding and not self.encoding:
                encoding = guess_json_utf(self.content)

            if encoding and self.encoding != encoding:
                self.encoding = encoding
        return self.encoding
