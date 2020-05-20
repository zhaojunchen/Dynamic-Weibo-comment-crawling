import requests
import os
import re
from bs4 import BeautifulSoup


def headers_to_dict(headers_str, out_put=True):
    items = headers_str.strip().split('\n')
    headers_dict = {}
    for t in items:
        key, value = re.findall(r'^(\S+):\s*([\s\S]+)$', t)[0]
        headers_dict[key] = value
        if out_put:
            print(f"'{key}': '{value}',")
    return headers_dict


# print(headers_to_dict(headers))
headers = {
    'Cookie': 'timezoneOffset=28800,0; _ga=GA1.2.687648836.1589170104; _gid=GA1.2.1271632368.1589170104; steamCountry=NL%7C46dd3f935bf539030fdf6b83d178cbf5; steamLoginSecure=76561199056627870%7C%7C64EA450ED70F68968F357C69C59C7D4ED647BF90; sessionid=ab9e5405286ff0be791cdf62; browserid=1452918551887061120; recentlyVisitedAppHubs=1213700%2C1145360%2C985890; app_impressions=985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_|985890@2_9_100010_',
    'Host': 'steamcommunity.com',
    'Referer': 'https://steamcommunity.com/app/985890/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=schinese',
    'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'X-Prototype-Version': '1.7'}

url = "https://steamcommunity.com/app/807120/reviews/?filterLanguage=schinese"
# requests的get请求 返回请求内容
response = requests.get(
   url)

# 解码为str串
html = response.content.decode("utf-8")
# soup 使用lxml解析
soup = BeautifulSoup(html, "lxml")
print(soup)

# 如何寻找规律
# 原始url https://steamcommunity.com/app/985890/reviews/?filterLanguage=schinese
# userreviewscursor=AoIIPyeWbH2%2F5oQC
# userreviewsoffset = (page-1)*10
# https://steamcommunity.com/app/985890/homecontent/?userreviewscursor=AoIIPyeWbH2%2F5oQC&userreviewsoffset=10&p=2&workshopitemspage=2&readytouseitemspage=2&mtxitemspage=2&itemspage=2&screenshotspage=2&videospage=2&artpage=2&allguidepage=2&webguidepage=2&integratedguidepage=2&discussionspage=2&numperpage=10&browsefilter=toprated&browsefilter=toprated&l=schinese&appHubSubSection=10&filterLanguage=schinese&searchText=
# https://steamcommunity.com/app/985890/homecontent/?userreviewscursor=AoIIPxoVd3zvvoQC&userreviewsoffset=20&p=3&workshopitemspage=3&readytouseitemspage=3&mtxitemspage=3&itemspage=3&screenshotspage=3&videospage=3&artpage=3&allguidepage=3&webguidepage=3&integratedguidepage=3&discussionspage=3&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=985890&appHubSubSection=10&appHubSubSection=10&l=schinese&filterLanguage=schinese&searchText=
# https://steamcommunity.com/app/985890/homecontent/?userreviewscursor=AoIIPxKZMXzBg4UC&userreviewsoffset=30&p=4&workshopitemspage=4&readytouseitemspage=4&mtxitemspage=4&itemspage=4&screenshotspage=4&videospage=4&artpage=4&allguidepage=4&webguidepage=4&integratedguidepage=4&discussionspage=4&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=985890&appHubSubSection=10&appHubSubSection=10&l=schinese&filterLanguage=schinese&searchText=
