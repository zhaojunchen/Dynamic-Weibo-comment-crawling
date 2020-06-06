import random
import bs4
import requests
import json
from bs4 import BeautifulSoup
import time
from urllib import parse

result = []
like = []
headers = {}
headers_str = """
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: no-cache
Connection: keep-alive
Cookie: _ga=GA1.2.956605479.1589971437; SCF=Aj1E_ydepWREVVJcOqZjRJziaqxHCYKn-Gv-RkCpdD3-yK0QtP9MXnGzRKqOklSAvFoDHGPZRikkC-e2p5i6hbM.; SINAGLOBAL=1876006436140.0298.1580887962558; SUB=_2AkMpmYbcdcPxrAZZkf8TymrmaYhH-jyaTO8qAn7uJhMyAxhu7nQ0qSVutBF-XFs9GyfhVYaW0Vs_ukVHTLppXU7j; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpV8GD3q0.RSonpeo.Re.5pSoeVqcv_; SUHB=0C1ydjo7snj-l2; UOR=,,www.baidu.com; login_sid_t=baa7692170c8e9d1ac377d5af586fc47; cross_origin_proto=SSL; TC-V5-G0=4de7df00d4dc12eb0897c97413797808; _s_tentry=-; Apache=8320276427423.147.1591405686498; ULV=1591405686518:20:6:6:8320276427423.147.1591405686498:1591365844522
Host: weibo.com
Pragma: no-cache
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36
"""


def init_headers(headers_string: str):
    headers_local = {}
    headers_string.strip()
    lines = headers_string.split('\n')
    for line in lines:
        if not line:
            continue
        line = line.strip()
        pos = line.index(":", 1)
        key = line[0:pos].strip()
        value = line[pos + 1:].strip()
        headers_local[key] = value
    return headers_local


# weibo format rnd timestamp
def __rnd():
    t = time.time()
    t = "{:.3f}".format(t).replace(".", "")
    return t


# ajax请求
def get_url(url: str):
    global result
    global like
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response)
        print("Ajax Response Error\n 尝试访问在IE更换Cookie")
        print("参考教程Cookie部分  https://github.com/zhaojunchen/Dynamic-Weibo-comment-crawling/tree/master/Weibo-comment")
        return None
    # print(response.status_code)
    if response.text == "":
        print("response is null")
        return None
    try:
        response = json.loads(response.text)
    except Exception as e:
        print(e, end=" ")
        print("response error")
        return None
    # 解析响应内容
    if response:
        soup = BeautifulSoup(response.get('data').get('html'), "lxml")
        # 解析评论内容
        comments = soup.find_all("div", attrs={"class": "WB_text"})
        # 评论字符串
        for comment in comments:
            s = "".join([t for t in comment.contents if type(t) == bs4.element.NavigableString])
            s = s.strip().replace("\n", "").lstrip("：").replace("等人", "").strip()
            if s:
                print(s)
                result.append(s)
            # https://www.zhihu.com/question/56861741

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
    print("热门mid")
    print(hot_mids)
    hot_ajax_start = []
    for mid in hot_mids:
        hot_ajax_start.append(
            "https://weibo.com/aj/v6/comment/big?ajwvr=6&id={0}&from=singleWeiBo&__rnd={1}".format(mid, __rnd()))
    return hot_ajax_start


# 起始url 延伸获取所有评论
def hot_ajax(url):
    while url:
        time.sleep(random.randint(1, 3))
        if url:
            print(url)
        url = get_url(url)


def start():
    global result
    result = []
    global headers
    headers = {}
    headers = init_headers(headers_str)
    # 测试请求头
    print(headers)
    search = input("请输入微博查询关键字：")
    search = search.strip()
    print("搜索请求为:" + search)
    # 获取每一个post的初始评论请求
    starts_ajax = get_hot_mid_by_search(search)
    for each in starts_ajax:
        print(each)
        # 请求完整的一级评论
        hot_ajax(each)
    print(len(result))
    with open("./" + search + ".txt", "w", encoding="utf-8") as f:
        f.write('\n'.join(result))
    return result


start()
