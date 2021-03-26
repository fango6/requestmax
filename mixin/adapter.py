from requests.adapters import HTTPAdapter
from requests.cookies import extract_cookies_to_jar
from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers

from .response import Response


class Adapter(HTTPAdapter):

    def build_response(self, req, resp):
        # only modified this
        response = Response()

        response.status_code = getattr(resp, 'status', None)

        response.headers = CaseInsensitiveDict(getattr(resp, 'headers', {}))

        response.encoding = get_encoding_from_headers(response.headers)
        response.raw = resp
        response.reason = response.raw.reason

        if isinstance(req.url, bytes):
            response.url = req.url.decode('utf-8')
        else:
            response.url = req.url

        extract_cookies_to_jar(response.cookies, req, resp)

        response.request = req
        response.connection = self
        response.encoding = response._guess_encoding()

        return response
