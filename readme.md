修改 requests 框架源码, 主要对其中的 response 增加了 `parsel.Selector` 和 `bs4.BeautifulSoup` 的功能.
并对 `parsel.Selector` 的 re 和 re_first 两个方法增加 `re.DOTALL` 匹配模式, 即增加多行匹配功能.

email: *`fango6@qq.com`*



## get 示例

`requestmax` 的使用方式和 `requests` 差不多, 但可以直接对 response 对象使用 xpath 和 find 等功能.

访问 https 的网站也不会告警了.

```python
import requestmax

def get_example():
    url = 'https://www.baidu.com'
    response = requestmax.get(url)
    print(response.text)
    # 使用 xpath
    print(response.xpath('//head/title/text()').get())
    # 可以多行匹配的正则
    print(response.re_first('百度.+知道'))
    # 贪婪模式
    print(response.re_first('百度.+?知道'))

get_example()
```



## 使用 session, 即处理 cookie 的示例

同时简单封装了一个 Request 类. 可以通过不同的参数来选择不同的功能, 比如可以通过 `cookie_enable` 参数来选择是否使用 session 功能.

```python
import requestmax

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

request_example()
```



## 设置默认代理示例

```python
from requestmax.utils import FetchProxiesAbstract

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
        # 返回 requests 支持的代理 ip 数据结构.
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

request_proxies_example()
```





没有发布 pypi, 可以本地安装

``` shell
cd requestmax/
python setup.py sdist
pip install .
rm -rf ./requestmax.egg-info ./dist
```

