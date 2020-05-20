import requests
import os
import re
from bs4 import BeautifulSoup
import random
from time import sleep


def get_app_id_list():
    temp = []
    app_id_list = []
    with open("app_id_list", "r") as f:
        temp = f.readlines()

    for i in temp:
        app_id_list.append(int(i.rstrip("\n")))

    review_list = []

    for i in app_id_list:
        review_list.append("https://steamcommunity.com/app/{0}/reviews/?filterLanguage=schinese".format(i))
    print(review_list)
    return app_id_list


app_id_list = get_app_id_list()


def randstr():
    # 第一种方法
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(16):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def ajax_str(app_id, page, key, offset=10):
    if offset != 10:
        offset = (page - 2) * 10 + offset
    else:
        offset = (page - 1) * 10
    site = {"app_id": app_id, "page": page, "offset": offset, "key": key}
    str = "https://steamcommunity.com/app/{app_id}/homecontent/?userreviewscursor={key}&userreviewsoffset={offset}&p={page}&workshopitemspage={page}&readytouseitemspage={page}&mtxitemspage={page}&itemspage={page}&screenshotspage={page}&videospage={page}&artpage={page}&allguidepage={page}&webguidepage={page}&integratedguidepage={page}&discussionspage={page}&numperpage=10&browsefilter=trendweek&browsefilter=trendweek&appid={app_id}&appHubSubSection=10&appHubSubSection=10&l=schinese&filterLanguage=schinese&searchText=".format(
        **site)
    return str


headers = {
    'Cookie': "browserid=1611670438598197465; timezoneOffset=28800,0; _ga=GA1.2.536334442.1589025061; Steam_Language=tchinese; steamCountry=JP%7Cd3450ae320e78a17bc80ab5f4194345b; sessionid=80a24383b2e9cde975c3e548; _gid=GA1.2.1197976376.1589372554; recentapps=%7B%22835570%22%3A1589373139%2C%221275250%22%3A1589372672%2C%22985890%22%3A1589177528%2C%221258080%22%3A1589177403%2C%22708770%22%3A1589170609%2C%221113410%22%3A1589170041%2C%221091500%22%3A1589169770%2C%221145360%22%3A1589110819%2C%22582010%22%3A1589025723%2C%221213700%22%3A1589025653%7D; app_impressions=253330@1_241_4_action_201|910490@1_241_4_action_43|397540@1_241_4_action_103|913060@1_241_4_action_103|1261970@1_241_4_action_103|985890@1_241_4_action_103|1147560@1_241_4_action_103|952060@1_241_4_action_103|835570@1_241_4_action_103|1134520@1_241_4_action_103|1090630@1_241_4_action_103|346010@1_5_9__300_5|444200@1_5_9__300_4|386360@1_5_9__300_3|8500@1_5_9__300_2|261550@1_5_9__300_1|910490@1_241_4_action_43|1147560@1_241_4_action_103|952060@1_241_4_action_103|835570@1_241_4_action_103|1134520@1_241_4_action_103|1090630@1_241_4_action_103|397540@1_241_4_action_103",
    'Host': 'steamcommunity.com',
    'Referer': 'https://steamcommunity.com/app/985890/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=schinese',
    'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'X-Prototype-Version': '1.7'}
# page start with 2

url = "https://steamcommunity.com/app/261550/homecontent/?userreviewscursor=AoIIPxCyEHGPgIcC&userreviewsoffset=10&p=2&workshopitemspage=2&readytouseitemspage=2&mtxitemspage=2&itemspage=2&screenshotspage=2&videospage=2&artpage=2&allguidepage=2&webguidepage=2&integratedguidepage=2&discussionspage=2&numperpage=10&browsefilter=trendweek&browsefilter=trendweek&l=schinese&appHubSubSection=10&filterLanguage=schinese&searchText="
# url = "https://steamcommunity.com/app/261550/homecontent/?userreviewscursor=AoIIPxCyEHGPgIQW&userreviewsoffset=10&p=2&workshopitemspage=2&readytouseitemspage=2&mtxitemspage=2&itemspage=2&screenshotspage=2&videospage=2&artpage=2&allguidepage=2&webguidepage=2&integratedguidepage=2&discussionspage=2&numperpage=10&browsefilter=trendweek&browsefilter=trendweek&l=schinese&appHubSubSection=10&filterLanguage=schinese&searchText="
# requests的get请求 返回请求内容
# 生成的关键随机数 是访问到元素的关键核心
# url = ajax_str(807120, 1)
# print(url)
# url = "https://steamcommunity.com/app/807120/homecontent/?userreviewscursor=AoIIAAAAAH/xroYC&userreviewsoffset=0&p=1&workshopitemspage=1&readytouseitemspage=1&mtxitemspage=1&itemspage=1&screenshotspage=1&videospage=1&artpage=1&allguidepage=1&webguidepage=1&integratedguidepage=1&discussionspage=1&numperpage=10&browsefilter=trendweek&browsefilter=trendweek&appid=807120&appHubSubSection=10&appHubSubSection=10&l=schinese&filterLanguage=schinese&searchText="
url = "https://steamcommunity.com/app/914010/reviews/?filterLanguage=schinese"


# response = requests.get(url)

# 解码为str串
# html = response.content.decode("utf-8")
# if not html:
#     print("respone is null")
#     exit(-1)
# soup 使用lxml解析
# soup = BeautifulSoup(html, "lxml")
# print(soup)
# like = soup.find_all("div", attrs={"class": "title"})
# comment = soup.find_all("div", attrs={"class": "apphub_CardTextContent"})
# key = soup.find("input", attrs={"name": "userreviewscursor"})
# if not key:
#     key = key.get("value")
#
# id = soup.find(attrs={"id": re.compile("page*")})
#
# # if id:
# #     id = id.get("id")
# # else:
# #     print("error")
# #     exit(-1)
#
#
# print("消息长度", len(comment))
# if (len(comment) != 10):
#     print("May be it is latest information")
# for i in comment:
#     # str = i.get_text().strip().split("\n")[-1].strip()
#     print(i.get_text().strip())
# for i in like:
#     print(i.get_text().strip())


# https://steamcommunity.com/app/985890/homecontent/?userreviewscursor=AoIIPxKZMXzBg4UC&userreviewsoffset=30&p=4&workshopitemspage=4&readytouseitemspage=4&mtxitemspage=4&itemspage=4&screenshotspage=4&videospage=4&artpage=4&allguidepage=4&webguidepage=4&integratedguidepage=4&discussionspage=4&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=985890&appHubSubSection=10&appHubSubSection=10&l=schinese&filterLanguage=schinese&searchText=
def parsereview(app_id):
    url = "https://steamcommunity.com/app/{0}/reviews/?filterLanguage=schinese".format(app_id)
    response = requests.get(url)
    # 解码为str串
    html = response.content.decode("utf-8")
    # if not html:
    #     print("respone is null")
    #     exit(-1)
    # soup 使用lxml解析
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    like = soup.find_all("div", attrs={"class": "title"})
    comment = soup.find_all("div", attrs={"class": "apphub_CardTextContent"})
    key = soup.find("input", attrs={"name": "userreviewscursor"})

    if key:
        key = key.get("value")
        return key
    else:
        return None


MAX = 1000000  #


def get_url(url, pos, neg):
    # url = "https://steamcommunity.com/app/{0}/reviews/?filterLanguage=schinese".format(app_id)
    print("url is {0}".format(url))
    response = requests.get(url)
    # 解码为str串
    html = response.content.decode("utf-8")
    if not html:
        print("respone is null")
        return "", -1
    # soup 使用lxml解析
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    key = soup.find("input", attrs={"name": "userreviewscursor"})
    if not key:
        return "", -1

    likes = soup.find_all("div", attrs={"class": "title"})
    comments = soup.find_all("div", attrs={"class": "apphub_CardTextContent"})
    neg_list = []
    pos_list = []
    length = -1
    if likes and comments:
        length = min(len(likes), len(comments))
        for i in range(0, length):
            like = likes[i].get_text().strip()
            comment = comments[i].get_text().strip().split("\n")[-1].strip()
            comment.replace("\n", "  ")
            if like == "推荐" or like =="Recommended":
                pos_list.append(comment + "\n")
            else:
                neg_list.append(comment + "\n")
    for i in pos_list:
        pos.write(i)
    for i in neg_list:
        neg.write(i)
    key = key.get("value")
    return key, length


def spider(app_id, path_prefix="./txt/"):
    print("\n\n\n\n\nApp " + str(app_id) + " start spider")
    all = 0
    with open(path_prefix + str(app_id) + "_pos.txt", 'w', encoding="utf-8") as pos, open(
            path_prefix + str(app_id) + "_neg.txt",
            'w', encoding="utf-8") as neg:

        url = "https://steamcommunity.com/app/{0}/reviews/?filterLanguage=schinese".format(app_id)
        key, length = get_url(url, pos, neg)
        all = all + length
        if length != 10:
            return all
        page = 2
        while key and length == 10:
            url = ajax_str(app_id, page, key)
            page += 1
            sleep(1.5)
            try:
                key, length = get_url(url, pos, neg)
            except Exception as e:
                print(e)
                return all
    print("App " + str(app_id) + " end spider")
    return all


all = 0
for app_id in app_id_list:
    print("appid is{0}  all mesage is {0}".format(app_id, all))
    spider(app_id)

# print("App " + str(app_id) + "\n\n\n\n\n")
# key = parsereview(app_id)
# if not key:
#     continue
# number_comment = 10
# for page in range(1, MAX):
#     url = ajax_str(app_id, page, key)
#     print(url)
#     # get dont need headers and cookies
#     response = requests.get(url)
#     html = response.content.decode("utf-8")
#     # print(html)
#     if not html:
#         if number_comment != 10:
#             print("appid {0} respone is null and must be end ".format(app_id))
#         else:
#             print("appid {0} respone is null and may be end ".format(app_id))
#         break
#     # soup 使用lxml解析
#     soup = BeautifulSoup(html, "lxml")
#     # like or dislike
#     like = soup.find_all("div", attrs={"class": "title"})
#     comment = soup.find_all("div", attrs={"class": "apphub_CardTextContent"})
#     key = soup.find("input", attrs={"name": "userreviewscursor"})
#     if key:
#         key = key.get("value")
#     else:
#         break
#     # id = soup.find(attrs={"id":re.compile("page*")}).get("id")
#     page_id = soup.find(attrs={"id": re.compile("page*")})
#     if page_id:
#         page_id = page_id.get("id")
#     else:
#         print("error occur")
#         break
#
#     number_comment = len(comment)
#     print("number result is {0}".format(number_comment))
#     for i in comment:
#         comment_str = i.get_text().strip().split("\n")[-1].strip()
#         print(comment_str)
#     for i in like:
#         like_str = i.get_text().strip()
#         print(like_str)
#
#     print("\n\n\n\n")
#     # time.sleep(2000)
