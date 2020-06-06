import threading

import bs4
import requests
import json
from bs4 import BeautifulSoup
import time
from urllib import parse

result = []
headers = {}
headers_str = """
   Accept: image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*'
   Accept-Encoding: gzip, deflate
   Accept-Language: zh-Hans-CN, zh-Hans; q=0.5
   Cookie: TC-V5-G0=595b7637c272b28fccec3e9d529f251a; Ugrow-G0=589da022062e21d675f389ce54f2eae7; TC-Page-G0=51e9db4bd1cd84f5fb5f9b32772c2750|1591066530|1591066487; wb_view_log=1280*8002; wb_view_log_5897661455=1280*8002; login_sid_t=61f6490b8854d9314ea281330ca8be54; cross_origin_proto=SSL; _s_tentry=www.weibo.com; Apache=3321810843863.0644.1591063441616; SUB=_2A25z0c5MDeRhGeNG4lUX9i_IzjmIHXVQpriErDV8PUNbmtAfLRPskW9NSuU4TFPwQjqTTtfPpJjZOPggz6ddH9z7; SSOLoginState=1591066144; UOR=,,graph.qq.com; wvr=6; SINAGLOBAL=8384493771349.852.1591017135494; __gads=ID=4793aec874b0ea09:T=1591017139:S=ALNI_MZxSwNGlcR2-JOmn0s4dy8OL-J4ZQ; ALF=1622602141; webim_unReadCount=%7B%22time%22%3A1591067155740%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A36%2C%22msgbox%22%3A0%7D; _gid=GA1.2.1084706662.1591017132; _ga=GA1.2.299669732.1591017132; ULV=1591063441737:2:2:2:3321810843863.0644.1591063441616:1591017135505; SUHB=00xZLEBODq7qr2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpX5KzhUgL.Fo-R1KMcSo2XSK-2dJLoI7_AIJepeoeXSKB7S5tt
   Host: www.weibo.com
   User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
   X-Requested-With: XMLHttpRequest
"""


def init_headers(headers_str: str):
    headers = {}
    headers_str.strip()
    lines = headers_str.split('\n')
    for line in lines:
        if not line:
            continue
        line = line.strip()
        pos = line.index(":", 1)
        key = line[0:pos].strip()
        value = line[pos + 1:].strip()
        headers[key] = value
    return headers


headers = init_headers(headers_str)


def __rnd():
    t = time.time()
    t = "{:.3f}".format(t).replace(".", "")
    return t


# ajax请求
def get_url(url: str, f=None):
    c = []
    print(headers)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response)
        print("Ajax Response Error\n 尝试访问在IE更换Cookie")
        print("参考教程Cookie部分  https://github.com/zhaojunchen/Dynamic-Weibo-comment-crawling/tree/master/Weibo-comment")
        return None
    print(response.status_code)
    if response.text == "":
        print("response is null")
        return None
    try:
        response = json.loads(response.text)
    except Exception as e:
        print(e, end=" ")
        print("response error")
        return None

    if response:
        soup = BeautifulSoup(response.get('data').get('html'), "lxml")
        comments = soup.find_all("div", attrs={"class": "WB_text"})
        for comment in comments:
            s = "".join([t for t in comment.contents if type(t) == bs4.element.NavigableString])
            s = s.strip().replace("\n", "").lstrip("：").replace("等人", "")
            if s:
                print(s)
                c.append(s + "\n")
            # https://www.zhihu.com/question/56861741
        if f:
            f.writelines(c)
        global result
        result += c
        action_data = soup.find("a", attrs={"action-type": "click_more_comment"})
        if not action_data:
            action_data = soup.find("div", attrs={"node-type": "comment_loading"})
            if not action_data:
                return None
        action_data = action_data.get("action-data").strip().replace("amp;", "")
        # print("action_data is " + action_data)
        dict = {"action_data": action_data, "rnd": __rnd()}
        if action_data:
            url = "https://weibo.com/aj/v6/comment/big?ajwvr=6&{action_data}&from=singleWeiBo&__rnd={rnd}".format(
                **dict)
        else:
            url = None
    return url


# 热门话题的url mid解析
def get_hot_by_search(url):
    response = requests.get(url)
    html = response.content.decode("utf-8")
    html = BeautifulSoup(html, "lxml")
    cards = html.find_all("div", attrs={"class": "card-wrap"})
    hot_mids = []
    for card in cards:
        titles = card.find_all("a")
        for title in titles:
            if title:
                if "热门" == title.text:
                    print(title.text)
                    hot_mids.append(card.get("mid"))
                    break
    print(hot_mids)
    return hot_mids


# 获取开始请求
def get_hot_mid_by_search(search: str):
    search = parse.quote(search)
    search = "https://s.weibo.com/hot?q=%23{0}%23".format(search)
    print(search)
    response = requests.get(search)
    html = response.content.decode("utf-8")
    html = BeautifulSoup(html, "lxml")
    cards = html.find_all("div", attrs={"class": "card-wrap"})
    hot_mids = []
    for card in cards:
        mid = card.get("mid")
        if mid:
            hot_mids.append(mid)
    print(hot_mids)
    hot_ajax_start = []
    for mid in hot_mids:
        hot_ajax_start.append(
            "https://weibo.com/aj/v6/comment/big?ajwvr=6&id={0}&from=singleWeiBo&__rnd={1}".format(mid, __rnd()))
    return hot_ajax_start


def hot_ajax(url):
    while url:
        time.sleep(1)
        url = get_url(url)


def start():
    search = input("请输入微博查询关键字：")
    search = search.strip()
    starts_ajax = get_hot_mid_by_search(search)
    i = -1
    for start in starts_ajax:
        print(start)
        hot_ajax(start)
    print(len(result))
    with open("./" + search + ".txt", "w", encoding="utf-8") as f:
        f.writelines(result)
    return result


start()

url = "https://www.weibo.com/aj/v6/comment/big?ajwvr=6&id=4510994850751735&from=singleWeiBo&__rnd=1591067169058"
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(response)
    print("Ajax Response Error\n 尝试访问在IE更换Cookie")
    print("参考教程Cookie部分  https://github.com/zhaojunchen/Dynamic-Weibo-comment-crawling/tree/master/Weibo-comment")
print(response.status_code)
response = response.text
json = json.loads(response)
soup = BeautifulSoup(json.get('data').get('html'), "lxml")
print(soup.prettify())
