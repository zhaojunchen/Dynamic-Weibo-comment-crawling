import requests
import os
from bs4 import BeautifulSoup

# requests的get请求 返回请求内容
response = requests.get('https://steamcommunity.com/app/1213700/reviews/?browsefilter=toprated&snr=1_5_100010_')

# 解码为str串
html = response.content.decode("utf-8")
# soup 使用lxml解析
soup = BeautifulSoup(html, "lxml")
print(soup)
comment = soup.find_all("div", attrs={"class": "apphub_CardTextContent"}, limits=10)
for i in comment:
    print("answer")
    print(i.get_text())

