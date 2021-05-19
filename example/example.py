import requestmax
from requestmax.utils import FetchProxiesAbstract


def get_example():
    url = 'https://www.baidu.com'
    response = requestmax.get(url)
    print(response.text)
    # 使用 xpath
    print(response.xpath('//head/title/text()').get())
    # 可以多行匹配的正则
    print(response.re_first('百度.+知道'))
    # 贪婪匹配
    print(response.re_first('百度.+?知道'))


def request_example():
    # verify=False: 不做 https 验证;
    # cookie_enable=True: 开启 session, 处理 cookie;
    # random_ua=True: 开启随机 user-agent 功能;
    # default_timeout=5: 默认请求的读写的超时时间为 5 秒钟;
    http = requestmax.Request(
        verify=False, cookie_enable=True, random_ua=True, default_timeout=5)

    url = 'https://www.baidu.com'
    headers = {
        "Host": "www.baidu.com",
    }
    response = http.get(url, headers=headers)
    print(response.text)
    # 使用 xpath
    print(response.xpath('//head/title/text()').get())
    # 可以多行匹配的正则
    print(response.re_first('百度.+知道'))
    # 贪婪匹配
    print(response.re_first('百度.+?知道'))


class FetchProxies(FetchProxiesAbstract):
    """
    获取代理的类, 该类必须实现 fetch_proxies 方法, 以便获取代理.
    """

    @property
    def kwargs(self):
        # 返回请求所携带的参数
        return {
            "method": "GET",
            "url": "http://proxy.io.com",
        }

    def fetch_proxies(self):
        # 返回代理 ip
        response = requestmax.request(**self.kwargs)
        ipv4 = response.text
        if ':' in ipv4:
            ipv4 = ipv4.split(':', 1)[0]
        if not requestmax.utils.is_ipv4_address(ipv4):
            raise TypeError("代理 ip 格式有误", response.text)
        return {
            "http": "http://{}".format(response.text.strip()),
            "https": "https://{}".format(response.text.strip()),
        }


def request_proxies_example():
    # fetch_proxies_cls: 设置获取代理实例, 必须实现 fetch_proxies 方法;
    http = requestmax.Request(
        verify=False, cookie_enable=True, random_ua=True,
        default_timeout=5, fetch_proxies_cls=FetchProxies(),
    )

    url = 'https://www.baidu.com'
    headers = {
        "Host": "www.baidu.com",
    }
    response = http.get(url, headers=headers)
    print(response.text)
    # 使用 xpath
    print(response.xpath('//head/title/text()').get())
    # 可以多行匹配的正则
    print(response.re_first('百度.+知道'))
    # 贪婪匹配
    print(response.re_first('百度.+?知道'))


if __name__ == "__main__":
    # get_example()
    request_example()
    # request_proxies_example()
