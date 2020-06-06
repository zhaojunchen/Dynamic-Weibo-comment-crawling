import weibospider

# li = weibospider.start("胡歌", 10)
# print(len(li))
import sys

# lines = sys.stdin.readlines()
headers_list = sys.stdin.readlines()
headers_str = "".join(headers_list).strip()
print(headers_str)
