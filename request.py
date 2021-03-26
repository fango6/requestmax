import sys

from requestmax.mixin import api, sessions
from requestmax.utils import default_headers, gen_ua


class Request:
    """
    verify: https 认证, 方便起见就默认成 False, 关闭认证了.
    cookie_enable: 命名参考了 scrapy, 要不要再下一个请求中延续使用 cookie.
    random_ua: 随机更换 user-agent.
    default_timeout: 默认请求超时时间.
    """

    def __init__(self, verify=False, cookie_enable=True, random_ua=False, default_timeout=10):
        if cookie_enable:
            self.sess = sessions.Session()
            self.sess.verify = verify
        else:
            self.sess = api
        self.verify = verify
        self.cookie_enable = cookie_enable
        self.random_ua = random_ua
        if random_ua:
            if sys.platform == "darwin":
                self._platform = "mac"
            elif "win" in sys.platform:
                self._platform = "win"
            else:
                self._platform = "linux"
        self.default_timeout = default_timeout

    def request(self, method, url,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):
        if timeout is None:
            timeout = self.default_timeout
        if verify is None:
            verify = self.verify
        if self.random_ua:
            headers = headers or {}
            ua_name = "User-Agent"
            ua_name_lower = ua_name.lower()
            ua_name = ua_name_lower if ua_name_lower in headers else ua_name
            headers[ua_name] = gen_ua(os=self._platform)
        return self.sess.request(
            method, url,
            params=params, data=data, headers=headers, cookies=cookies, files=files,
            auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
            hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def get(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def options(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)
