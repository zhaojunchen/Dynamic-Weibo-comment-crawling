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


headers  ="""

"""
headers_to_dict()