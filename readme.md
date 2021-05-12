修改 requests 框架源码, 主要对 response 增加 `Selector` 和 `bs4.BeautifulSoup` 的解析函数.
并对 Selector 的 re 和 re_first 方法增加 `re.DOTALL` 匹配, 使其可以匹配多行.

email: *`fango8888@163.com`*



使用方式和 `requests` 差不多, 但可以直接对 response 对象使用 xpath 和 find 等功能.

```python
import requestmax

def get_simple():
    url = 'https://www.baidu.com'
    response = requestmax.get(url)
    print(response.text)
    # 使用 xpath
    print(response.xpath('//head/title/text()').get())
    # 可以多行匹配的正则
    print(response.re_first('百度.+知道'))
    # 贪婪模式
    print(response.re_first('百度.+?知道'))

```



同时简单封装了一个 Request 类.

```python
import requestmax

def request_simple():
    """
    verify: 是否验证服务器的 SSL 证书, 默认 False 即否.
    cookie_enable: 是否要处理 cookies.
    random_ua: 随机更换 user-agent.
    default_timeout: 默认请求超时时间.
    default_proxies: 默认请求代理.
    """
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
    # 贪婪模式
    print(response.re_first('百度.+?知道'))

```



访问 https 协议的网站也不会告警了.



没有发布 pypi, 可以本地安装

``` shell
cd requestmax/
python setup.py sdist
pip install .
rm -rf ./requestmax.egg-info ./dist
```

