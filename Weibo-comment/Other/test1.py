import bs4
from bs4 import BeautifulSoup

html = """
<div class="friendBlockContent">
        Bartdavy<br>
        <span class="friendSmallText">
            Online
        </span>
</div>
        
"""
soup = BeautifulSoup(html, "lxml")
div = soup.find("div")
s = "".join([t for t in div.contents if type(t) == bs4.element.NavigableString])
print(type(s))
print("".join([t for t in div.contents if type(t) == bs4.element.NavigableString]))
# print(s)
# print(div.text)

headers_morecomment = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: no-cache
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Cookie: SINAGLOBAL=1876006436140.0298.1580887962558; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpX5KMhUgL.Fo-R1KMcSo2XSK-2dJLoI7_AIJepeoeXSKB7S5tt; SUHB=0k1ydATVxcJbOB; ALF=1621482566; SSOLoginState=1589946566; SCF=Aj1E_ydepWREVVJcOqZjRJziaqxHCYKn-Gv-RkCpdD3-YldEFyl-0XchCmIJeuusa6ZAKkU-yDcXde9nmtoty_w.; SUB=_2A25zwNiXDeRhGeNG4lUX9i_IzjmIHXVQtE1frDV8PUNbmtAKLRfNkW9NSuU4TCkz_zksAdhnrBX8N-Bb38C6qA6v; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=5136918982924.055.1589946568812; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20; ULV=1589946568931:12:7:2:5136918982924.055.1589946568812:1589713055557; Ugrow-G0=d52660735d1ea4ed313e0beb68c05fc5; wb_view_log_5897661455=1280*8002; wvr=6; webim_unReadCount=%7B%22time%22%3A1589955445163%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A38%2C%22msgbox%22%3A0%7D; TC-Page-G0=8dc78264df14e433a87ecb460ff08bfe|1589955446|1589955446
Host: weibo.com
Pragma: no-cache
Referer: https://weibo.com/5654266820/J2vIszRTV?type=comment
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36
X-Requested-With: XMLHttpRequest
"""

import re
def headers_to_dict(headers_str, out_put=True):
    items = headers_str.strip().split('\n')
    headers_dict = {}
    for t in items:
        key, value = re.findall(r'^(\S+):\s*([\s\S]+)$', t)[0]
        headers_dict[key] = value
        if out_put:
            print(f"'{key}': '{value}',")
    return headers_dict

print(headers_to_dict(headers_morecomment))
# from urllib import parse
# search = "刘亦菲"
# search = parse.quote(search)
# print(search)