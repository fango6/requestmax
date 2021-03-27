from urllib3 import disable_warnings

from requestmax.mixin import api, sessions
from requestmax.utils import fetch_proxies_by_url, gen_ua, get_platform

disable_warnings()


def set_default_proxies(default_proxies):
    # self.default_proxies is callable
    if isinstance(default_proxies, dict):
        # 已经设置了正确的代理格式
        return lambda: default_proxies
    elif isinstance(default_proxies, str) and '@' in default_proxies:
        # 独享代理/ 用户认证
        return lambda: {
            "http": "http://{}".format(default_proxies),
            "https": "https://{}".format(default_proxies),
        }
    elif default_proxies:
        # 从代理池中获取, 会请求链接
        return fetch_proxies_by_url
    return None


class Request:
    """
    @desc: hook requests.Session.
    @params:
        verify: 是否验证服务器的 SSL 证书, 默认 False 即否.
        cookie_enable: 是否要处理 cookies.
        random_ua: 随机更换 user-agent.
        default_timeout: 默认请求超时时间.
        default_proxies: 默认请求代理.
    """

    def __init__(self, verify=False, cookie_enable=True, random_ua=False, default_timeout=10, default_proxies=None):
        self.verify = verify
        self.cookie_enable = cookie_enable
        if cookie_enable:
            self.sess = sessions.Session()
            self.sess.verify = verify
        else:
            self.sess = api

        self.random_ua = random_ua
        # only set self._platform attribute when random_ua is True
        if random_ua:
            self._platform = get_platform()

        # setting request default timeout.
        self.default_timeout = default_timeout
        # setting request default proxies.
        self.default_proxies = set_default_proxies(default_proxies)

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
        if proxies is None and callable(self.default_proxies):
            proxies = self.default_proxies()
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
