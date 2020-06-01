headers = """
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


print(init_headers(headers))
