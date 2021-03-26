from collections import OrderedDict

import requests
from requestmax.mixin.adapter import Adapter
from requestmax.utils import default_headers
from requests.cookies import cookiejar_from_dict
from requests.hooks import default_hooks
from requests.models import DEFAULT_REDIRECT_LIMIT


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
