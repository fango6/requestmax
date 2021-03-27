from collections import OrderedDict

import requests
from requestmax.mixin.adapter import Adapter
from requests.cookies import cookiejar_from_dict
from requests.hooks import default_hooks
from requests.models import DEFAULT_REDIRECT_LIMIT
from requests.structures import CaseInsensitiveDict
from urllib3 import disable_warnings

disable_warnings()


def default_headers():
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    })


class Session(requests.Session):

    def __init__(self):
        # use my default_headers
        self.headers = default_headers()

        self.auth = None

        self.proxies = {}

        self.hooks = default_hooks()

        self.params = {}

        self.stream = False

        self.verify = True

        self.cert = None

        self.max_redirects = DEFAULT_REDIRECT_LIMIT

        self.trust_env = True

        self.cookies = cookiejar_from_dict({})

        self.adapters = OrderedDict()
        # modify HTTPAdapter to Adapter
        self.mount('https://', Adapter())
        self.mount('http://', Adapter())
