import threading

import bs4
import requests
import json
import os
from bs4 import BeautifulSoup
import time
import re
from urllib import parse


def headers_to_dict(headers_str, out_put=True):
    items = headers_str.strip().split('\n')
    headers_dict = {}
    for t in items:
        key, value = re.findall(r'^(\S+):\s*([\s\S]+)$', t)[0]
        headers_dict[key] = value
        if out_put:
            print(f"'{key}': '{value}',")
    return headers_dict


def __rnd():
    t = time.time()
    t = "{:.3f}".format(t).replace(".", "")
    return t


lock = threading.Lock()  # 申请一把锁
comments = []

cookies = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: no-cache
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Cookie: SINAGLOBAL=1876006436140.0298.1580887962558; wvr=6; wb_view_log_5897661455=1280*8002; wb_view_log=1280*8002; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpX5KMhUgL.Fo-R1KMcSo2XSK-2dJLoI7_AIJepeoeXSKB7S5tt; UOR=,,login.sina.com.cn; ALF=1620706670; SSOLoginState=1589170674; SCF=Aj1E_ydepWREVVJcOqZjRJziaqxHCYKn-Gv-RkCpdD3-qPjj5OGRm4zjp28NrcopfXDL3J6V-Tp42k5YlmxcGh0.; SUB=_2A25zvKGiDeRhGeNG4lUX9i_IzjmIHXVQy5RqrDV8PUNbmtAKLXCgkW9NSuU4TGgS9sokUkd48UmhHeXafoUr0XBI; SUHB=0ebdCieu1NY9fA; Ugrow-G0=e1a5a1aae05361d646241e28c550f987; _s_tentry=login.sina.com.cn; Apache=1996585863791.549.1589170675451; ULV=1589170675474:9:4:4:1996585863791.549.1589170675451:1589169934090; TC-V5-G0=595b7637c272b28fccec3e9d529f251a; webim_unReadCount=%7B%22time%22%3A1589170913727%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A37%2C%22msgbox%22%3A0%7D; TC-Page-G0=7f6863db1952ff8adac0858ad5825a3b|1589170919|1589170669
Host: weibo.com
Pragma: no-cache
Referer: https://weibo.com/3165034955/J1aeZFLwk?filter=hot&root_comment_id=0&type=comment
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36
X-Requested-With: XMLHttpRequest
"""
# print(headers_to_dict(cookies))

# 修改cookies得到新的请求  在合适的浏览器copy出请求的参数
headers_ajax = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'SINAGLOBAL=1876006436140.0298.1580887962558; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpX5KMhUgL.Fo-R1KMcSo2XSK-2dJLoI7_AIJepeoeXSKB7S5tt; SUHB=0k1ydATVxcJbOB; ALF=1621482566; SSOLoginState=1589946566; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=5136918982924.055.1589946568812; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20; ULV=1589946568931:12:7:2:5136918982924.055.1589946568812:1589713055557; Ugrow-G0=d52660735d1ea4ed313e0beb68c05fc5; wb_view_log_5897661455=1280*8002; wvr=6; TC-Page-G0=45685168db6903150ce64a1b7437dbbb|1589956393|1589956389; webim_unReadCount=%7B%22time%22%3A1589959710838%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A38%2C%22msgbox%22%3A0%7D',
                'Host': 'weibo.com',
                'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
                }

headers_comment = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Cookie': 'SINAGLOBAL=1876006436140.0298.1580887962558; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpX5KMhUgL.Fo-R1KMcSo2XSK-2dJLoI7_AIJepeoeXSKB7S5tt; SUHB=0k1ydATVxcJbOB; ALF=1621482566; SSOLoginState=1589946566; SCF=Aj1E_ydepWREVVJcOqZjRJziaqxHCYKn-Gv-RkCpdD3-YldEFyl-0XchCmIJeuusa6ZAKkU-yDcXde9nmtoty_w.; SUB=_2A25zwNiXDeRhGeNG4lUX9i_IzjmIHXVQtE1frDV8PUNbmtAKLRfNkW9NSuU4TCkz_zksAdhnrBX8N-Bb38C6qA6v; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=5136918982924.055.1589946568812; ULV=1589946568931:12:7:2:5136918982924.055.1589946568812:1589713055557; wvr=6; webim_unReadCount=%7B%22time%22%3A1589954335956%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A38%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined',
                   'Host': 's.weibo.com',
                   'Referer': 'https://s.weibo.com/weibo?q=%E5%88%98%E4%BA%A6%E8%8F%B2&xsort=hot&Refer=hotmore',
                   'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}

myheadrs = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'SINAGLOBAL=1876006436140.0298.1580887962558; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpX5KMhUgL.Fo-R1KMcSo2XSK-2dJLoI7_AIJepeoeXSKB7S5tt; SUHB=0k1ydATVxcJbOB; ALF=1621482566; SSOLoginState=1589946566; SCF=Aj1E_ydepWREVVJcOqZjRJziaqxHCYKn-Gv-RkCpdD3-YldEFyl-0XchCmIJeuusa6ZAKkU-yDcXde9nmtoty_w.; SUB=_2A25zwNiXDeRhGeNG4lUX9i_IzjmIHXVQtE1frDV8PUNbmtAKLRfNkW9NSuU4TCkz_zksAdhnrBX8N-Bb38C6qA6v; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=5136918982924.055.1589946568812; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20; ULV=1589946568931:12:7:2:5136918982924.055.1589946568812:1589713055557; Ugrow-G0=d52660735d1ea4ed313e0beb68c05fc5; wb_view_log_5897661455=1280*8002; wvr=6; webim_unReadCount=%7B%22time%22%3A1589955445163%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A38%2C%22msgbox%22%3A0%7D; TC-Page-G0=8dc78264df14e433a87ecb460ff08bfe|1589955446|1589955446',
            'Host': 'weibo.com', 'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}


# print(headers)

# url = "https://s.weibo.com/weibo?q=%E5%88%98%E4%BA%A6%E8%8F%B2&"

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


#
# hot_urls = (get_hot_by_search(url))
# url = hot_urls[0]


def get_start_ajax(url):
    print("get first url")
    response = requests.get(url, headers=headers_ajax)
    s = response.content.decode("utf-8")
    html = json.loads(s)
    if not html:
        return None
    html = html.get("data").get("html")
    html = BeautifulSoup(html, "lxml")
    more = html.find("div", attrs={"class": "card-more-a"})
    url = more.a.get("href")
    return "https:{0}?type=comment#_rnd{1}".format(url, __rnd())


# get_start_ajax(url)


# ajax请求
def get_url(url: str, f=None, headers=headers_ajax):
    c = []
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Ajax Response Error")
        return None
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
        with lock:
            comments += c
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


# url = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4505985768548679&from=singleWeiBo&__rnd={0}".format(__rnd())
# while url:
#     # print(url)
#     url = get_url(url)
# __rnd()


# https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4505985768548679&from=singleWeiBo&__rnd=1589955292328


# 输出查询的内容 输出热门话题的mid

class myThread(threading.Thread):

    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url

    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                hot_ajax(self.url)
            except Exception as e:
                print(e)
                print("异常")
                break
        print("Exiting " + self.name)


def hot_ajax(url):
    while url:
        time.sleep(1)
        url = get_url(url)


def run(search):
    starts_ajax = get_hot_mid_by_search(search)
    i = -1
    threads = []
    for start in starts_ajax:
        i = i + 1
        thread = myThread(start, "threading-" + str(i))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    search = "魏晨结婚"
    starts_ajax = get_hot_mid_by_search(search)
    i = -1
    threads = []
    for start in starts_ajax:
        print(start)
        hot_ajax(start)
    #     i = i + 1
    #     thread = myThread(start, "threading-" + str(i))
    #     threads.append(thread)
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    print(len(comments))
    with open("./" + "search" + ".txt", "w", encoding="utf-8") as f:
        f.writelines(comments)
