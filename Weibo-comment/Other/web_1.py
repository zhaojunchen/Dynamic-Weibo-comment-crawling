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

# 修改cookies得到新的请求  在合适的浏览器copy出请求的参数
headers = {
    'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'Keep-Alive',
    'Cookie': 'SUB=_2AkMpmGNfdcPxrAZZkf8TymrmaYhH-jyaTQqpAn7uJhMyAxh77lUCqSVutBF-XEcZoLdAAUhhdFH_OTIESN5YwCgm; _s_tentry=-; Apache=8383124929170.817.1589954045328; TC-V5-G0=4de7df00d4dc12eb0897c97413797808; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; TC-Page-G0=62b98c0fc3e291bc0c7511933c1b13ad|1589963875|1589963875; UOR=,,login.sina.com.cn; SINAGLOBAL=7390078349060.063.1589116949157; webim_unReadCount=%7B%22time%22%3A1589963878449%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A39%2C%22msgbox%22%3A0%7D; ULV=1589954045516:5:5:3:8383124929170.817.1589954045328:1589727942460; SUHB=0nleBnbCAt0qZa; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpV8GD3q0.RSonpeo.Re.5pSoeVqcv_; wb_view_log_5897661455=1280*8002; login_sid_t=cf5e8bd6bb1862b4dacf3cdf346c4223; cross_origin_proto=SSL; WBStorage=42212210b087ca50|undefined; wb_view_log=1280*8002',
    'Host': 'weibo.com',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'
}


def __rnd():
    t = time.time()
    t = "{:.3f}".format(t).replace(".", "")
    return t


# ajax请求
def get_url(url: str, f=None, headers=headers):
    c = []
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Ajax Response Error")
        return None
    response = json.loads(response.text)
    if response:
        soup = BeautifulSoup(response.get('data').get('html'), "lxml")
        print(soup)
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
    print(html)
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
    search = "https://s.weibo.com/weibo?q={0}&".format(search)
    print(search)
    hot_mids = get_hot_by_search(search)
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
    cookie = "_s_tentry=-; Apache=8383124929170.817.1589954045328; TC-V5-G0=4de7df00d4dc12eb0897c97413797808; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; TC-Page-G0=62b98c0fc3e291bc0c7511933c1b13ad|1589963875|1589963875; UOR=,,login.sina.com.cn; SINAGLOBAL=7390078349060.063.1589116949157; webim_unReadCount=%7B%22time%22%3A1589963878449%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A39%2C%22msgbox%22%3A0%7D; ULV=1589954045516:5:5:3:8383124929170.817.1589954045328:1589727942460; SUHB=0nleBnbCAt0qZa; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpV8GD3q0.RSonpeo.Re.5pSoeVqcv_; wb_view_log_5897661455=1280*8002; login_sid_t=cf5e8bd6bb1862b4dacf3cdf346c4223; cross_origin_proto=SSL; WBStorage=42212210b087ca50|undefined; wb_view_log=1280*8002"
    cookie = None
    if cookie:  # document.cookie
        headers["Cookie"] = cookie
    print(headers)
    search = "魏晨结婚"
    starts_ajax = get_hot_mid_by_search(search)
    i = -1
    threads = []
    for start in starts_ajax:
        print(start)
        hot_ajax(start)
    print(len(result))
    with open("./" + "search" + ".txt", "w", encoding="utf-8") as f:
        f.writelines(result)
