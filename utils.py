import socket
import sys

import requests
from user_agent import generate_user_agent


def get_platform():
    ''' 获取操作系统标识, 以用作 gen_ua 函数的 os 参数
    '''
    if sys.platform == "darwin":
        return "mac"
    elif "win" in sys.platform:
        return "win"
    return "linux"


def gen_ua(os=None, device_type=None, navigator=None, platform=None):
    '''
    @params:
        os: ("win", "mac", "linux")
        device_type: ("desktop", "smartphone", "tablet", "all")
        platform: like "Windows NT 5.1; WOW64"
    '''
    return generate_user_agent(os, device_type=device_type, navigator=navigator, platform=platform)


def is_ipv4_address(string_ip):
    """
    :rtype: bool
    """
    try:
        socket.inet_aton(string_ip)
    except socket.error:
        return False
    return True


class FetchProxiesAbstract:

    @property
    def kwargs(self) -> dict:
        """
        @return: 请求所携带的参数
        """
        raise NotImplementedError

    def fetch_proxies(self) -> dict:
        """
        @return: 返回代理 ip.
        """
        raise NotImplementedError


class FetchProxies(FetchProxiesAbstract):
    """
    获取代理的类, 该类必须实现 fetch_proxies 方法, 以便获取代理.
    """

    @property
    def kwargs(self):
        return {
            "proxy_url": "http://proxy.io.com",
            "method": "GET",
        }

    def fetch_proxies(self):
        response = requests.request(**self.kwargs)
        ipv4 = response.text
        if ':' in ipv4:
            ipv4 = ipv4.split(':', 1)[0]
        if not is_ipv4_address(ipv4):
            raise TypeError("代理 ip 格式有误", response.text)
        return {
            "http": "http://{}".format(response.text.strip()),
            "https": "https://{}".format(response.text.strip()),
        }
