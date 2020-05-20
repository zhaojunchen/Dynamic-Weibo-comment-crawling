import random

import requests
import os
import re
from bs4 import BeautifulSoup

headers = {
    'Cookie': "browserid=1611670438598197465; timezoneOffset=28800,0; _ga=GA1.2.536334442.1589025061; Steam_Language=tchinese; steamCountry=JP%7Cd3450ae320e78a17bc80ab5f4194345b; sessionid=80a24383b2e9cde975c3e548; _gid=GA1.2.1197976376.1589372554; recentapps=%7B%22835570%22%3A1589373139%2C%221275250%22%3A1589372672%2C%22985890%22%3A1589177528%2C%221258080%22%3A1589177403%2C%22708770%22%3A1589170609%2C%221113410%22%3A1589170041%2C%221091500%22%3A1589169770%2C%221145360%22%3A1589110819%2C%22582010%22%3A1589025723%2C%221213700%22%3A1589025653%7D; app_impressions=253330@1_241_4_action_201|910490@1_241_4_action_43|397540@1_241_4_action_103|913060@1_241_4_action_103|1261970@1_241_4_action_103|985890@1_241_4_action_103|1147560@1_241_4_action_103|952060@1_241_4_action_103|835570@1_241_4_action_103|1134520@1_241_4_action_103|1090630@1_241_4_action_103|346010@1_5_9__300_5|444200@1_5_9__300_4|386360@1_5_9__300_3|8500@1_5_9__300_2|261550@1_5_9__300_1|910490@1_241_4_action_43|1147560@1_241_4_action_103|952060@1_241_4_action_103|835570@1_241_4_action_103|1134520@1_241_4_action_103|1090630@1_241_4_action_103|397540@1_241_4_action_103",
    'Host': 'steamcommunity.com',
    'Referer': 'https://steamcommunity.com/app/985890/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=schinese',
    'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'X-Prototype-Version': '1.7'}

urls = {"https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/",
        "https://store.steampowered.com/tags/zh-tw/%E4%BC%91%E9%96%92/",
        "https://store.steampowered.com/tags/zh-tw/%E5%A4%A7%E5%9E%8B%E5%A4%9A%E4%BA%BA%E9%80%A3%E7%B7%9A/",
        "https://store.steampowered.com/tags/zh-tw/%E5%86%92%E9%9A%AA/",
        "https://store.steampowered.com/tags/zh-tw/%E7%AD%96%E7%95%A5/",
        "https://store.steampowered.com/tags/zh-tw/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/",
        "https://store.steampowered.com/tags/zh-tw/%E9%81%8B%E5%8B%95/"
        }
url = "https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/"
list_app_id = []
for url in urls:
    # requests的get请求 返回请求内容
    response = requests.get(
        url)

    # 解码为str串
    html = response.content.decode("utf-8")
    # soup 使用lxml解析
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    a_list = soup.find_all('a', attrs={"class": "tab_item"})
    for a in a_list:
        list_app_id.append(a.get("data-ds-appid"))

print(list_app_id)
random.shuffle(list_app_id)
with open("app_id_list", "w") as f:
    for i in list_app_id:
        f.write(i + "\n")