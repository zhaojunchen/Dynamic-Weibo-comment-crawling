# https://weibo.cn/comment/J1ffa3Q1A?uid=3725773862&rl=1
# domain = "https://weibo.cn/"
# 参考教程 https://blog.csdn.net/weixin_42555080/article/details/88363040
import requests
import os
from bs4 import BeautifulSoup

# requests的get请求 返回请求内容
response = requests.get('https://weibo.cn/comment/J1ffa3Q1A?uid=3725773862&rl=1')

# 解码为str串
html = response.content.decode("utf-8")
print(html)
# 解决爬取问题！
