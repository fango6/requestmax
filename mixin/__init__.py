"""
修改 requests 框架源码, 主要对 response 增加 Selector 和 bs4.BeautifulSoup 的解析函数.
并对 Selector 的 re 和 re_first 方法增加 re.DOTALL 匹配, 使其可以匹配多行.
"""
