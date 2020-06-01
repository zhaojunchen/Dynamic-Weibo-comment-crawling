import threading

import bs4
import requests
import json
import os
from bs4 import BeautifulSoup
import time
import re
from urllib import parse

lock = threading.Lock()  # 申请一把锁
result = []
global headers
headers_str = """
      Accept: text/html, application/xhtml+xml, image/jxr, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-Hans-CN, zh-Hans; q=0.5
Cookie: SINAGLOBAL=8384493771349.852.1591017135494; __gads=ID=4793aec874b0ea09:T=1591017139:S=ALNI_MZxSwNGlcR2-JOmn0s4dy8OL-J4ZQ; _gid=GA1.2.1084706662.1591017132; _ga=GA1.2.299669732.1591017132; ULV=1591017135505:1:1:1:8384493771349.852.1591017135494:; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5y8TGGKcjNbhXKfILZ2066; SUB=_2AkMpiHCGf8NxqwJRmf4dz2rlao52yQDEieKf1IFdJRMxHRl-yT92qnwHtRB6AgheaYPIkmnFYP2X5LOxHmDcgGsoHgGK; login_sid_t=a709781483e744c49335973eb806fae2; cross_origin_proto=SSL; _s_tentry=-; Apache=8384493771349.852.1591017135494; Ugrow-G0=6fd5dedc9d0f894fec342d051b79679e; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20
Host: www.weibo.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
"""


def init_headers(headers: str):
    headers_dict = {}
    headers.strip()
    lines = headers.split('\n')
    for line in lines:
        if not line:
            continue
        line = line.strip()
        pos = line.find(":")
        key = line[0:pos].strip()
        value = line[pos + 1:].strip()
        headers_dict[key] = value
    return headers_dict


headers = init_headers(headers_str)


def __rnd():
    t = time.time()
    t = "{:.3f}".format(t).replace(".", "")
    return t


# ajax请求
def get_url(url: str, f=None):
    c = []
    # print(headers)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response)
        print("Ajax Response Error\n 尝试访问在IE更换Cookie")
        print("参考教程Cookie部分  https://github.com/zhaojunchen/Dynamic-Weibo-comment-crawling/tree/master/Weibo-comment")
        return None
    # print(response.text)
    response = json.loads(response.text)

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
        with lock:
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
def get_hot_mid_by_search_3(search: str):
    search = parse.quote(search)
    search = "https://s.weibo.com/weibo?q={0}&".format(search)
    print(search)
    hot_mids = get_hot_by_search(search)
    print(hot_mids)
    hot_ajax_start = []
    for mid in hot_mids:
        hot_ajax_start.append(
            "https://weibo.com/aj/v6/comment/big?ajwvr=6&id={0}&from=singleWeiBo&__rnd={1}".format(mid, __rnd()))
    return hot_ajax_start


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
        hot_mids.append(card.get("mid"))
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


if __name__ == '__main__':
    print(headers)
    search = input("请输入微博查询关键字：")
    search = search.strip()
    starts_ajax = get_hot_mid_by_search(search)
    i = -1
    threads = []
    for start in starts_ajax:
        print(start)
        hot_ajax(start)
    print(len(result))
    with open("./" + search + ".txt", "w", encoding="utf-8") as f:
        f.writelines(result)
