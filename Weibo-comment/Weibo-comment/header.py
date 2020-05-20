import re

headers = {
    'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'Keep-Alive',
    'Cookie': 'SUB=_2AkMpmGNfdcPxrAZZkf8TymrmaYhH-jyaTQqpAn7uJhMyAxh77lUCqSVutBF-XEcZoLdAAUhhdFH_OTIESN5YwCgm; _s_tentry=-; Apache=8383124929170.817.1589954045328; TC-V5-G0=4de7df00d4dc12eb0897c97413797808; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; TC-Page-G0=62b98c0fc3e291bc0c7511933c1b13ad|1589963875|1589963875; UOR=,,login.sina.com.cn; SINAGLOBAL=7390078349060.063.1589116949157; webim_unReadCount=%7B%22time%22%3A1589963878449%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A39%2C%22msgbox%22%3A0%7D; ULV=1589954045516:5:5:3:8383124929170.817.1589954045328:1589727942460; SUHB=0nleBnbCAt0qZa; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpV8GD3q0.RSonpeo.Re.5pSoeVqcv_; wb_view_log_5897661455=1280*8002; login_sid_t=cf5e8bd6bb1862b4dacf3cdf346c4223; cross_origin_proto=SSL; WBStorage=42212210b087ca50|undefined; wb_view_log=1280*8002',
    'Host': 'weibo.com',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'
}


def headers_to_dict(headers_str, out_put=True):
    items = headers_str.strip().split('\n')
    headers_dict = {}
    for t in items:
        key, value = re.findall(r'^(\S+):\s*([\s\S]+)$', t)[0]
        headers_dict[key] = value
        if out_put:
            print(f"'{key}': '{value}',")
    return headers_dict


print(headers_to_dict(headers))
