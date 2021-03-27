import requestmax


def get_simple():
    url = 'https://www.baidu.com'
    response = requestmax.get(url)
    print(response.text)
    # 使用 xpath
    print(response.xpath('//head/title/text()').get())
    # 可以多行匹配的正则
    print(response.re_first('百度.+知道'))
    # 贪婪匹配
    print(response.re_first('百度.+?知道'))


def request_simple():
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


if __name__ == "__main__":
    # get_simple()
    request_simple()
