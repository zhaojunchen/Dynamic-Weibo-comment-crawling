# 教程概览 https://blog.csdn.net/huangbaokang/article/details/83503677
# 教程文档 https://github.com/easonhan007/webdriver_guide/blob/master/README.md
# 元素定位和点击事件 https://github.com/easonhan007/webdriver_guide/blob/master/08/simple_locate.py.md
# 打开浏览器

from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException


# 实现页面自动下移
def scroll(driver):
    # 获取当前页面滚动条纵坐标的位置
    driver.execute_script(""" 
        (function () { 
            var y = document.documentElement.scrollTop; 
            var step = 100; 
            window.scroll(0, y); 
            function f() { 
                if (y < document.body.scrollHeight) { 
                    y += step; 
                    window.scroll(0, y); 
                    setTimeout(f, 50); 
                }
                else { 
                    window.scroll(0, y); 
                } 
            } 
            setTimeout(f, 1000); 
        })(); 
        """)


def str_to_cookies_dict(str):
    str = str.replace("=", "':'")
    str = str.replace(";", "':'")
    return str



cookies = {
    'SINAGLOBAL': '1876006436140.0298.1580887962558', 'wvr': '6', 'wb_view_log_5897661455': '1280*8002',
    'wb_view_log': '1280*8002',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFM0ZAQ0We2E62STc0UE.Bl5JpX5KMhUgL.Fo-R1KMcSo2XSK-2dJLoI7_AIJepeoeXSKB7S5tt',
    'UOR': ',,login.sina.com.cn', 'ALF': '1620706670', 'SSOLoginState': '1589170674',
    'SCF': 'Aj1E_ydepWREVVJcOqZjRJziaqxHCYKn-Gv-RkCpdD3-qPjj5OGRm4zjp28NrcopfXDL3J6V-Tp42k5YlmxcGh0.',
    'SUB': '_2A25zvKGiDeRhGeNG4lUX9i_IzjmIHXVQy5RqrDV8PUNbmtAKLXCgkW9NSuU4TGgS9sokUkd48UmhHeXafoUr0XBI',
    'SUHB': '0ebdCieu1NY9fA', 'Ugrow-G0': 'e1a5a1aae05361d646241e28c550f987', '_s_tentry': 'login.sina.com.cn',
    'Apache': '1996585863791.549.1589170675451',
    'ULV': '1589170675474:9:4:4:1996585863791.549.1589170675451:1589169934090',
    'TC-V5-G0': '595b7637c272b28fccec3e9d529f251a',
    'webim_unReadCount': '%7B%22time%22%3A1589170913727%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A37%2C%22msgbox%22%3A0%7D',
    'TC-Page-G0': '7f6863db1952ff8adac0858ad5825a3b|1589170919|1589170669'}

# 打开浏览器
dr = webdriver.Chrome()
# 最大化浏览器
dr.maximize_window()
# 设置大小
url = 'https://weibo.com/3165034955/J1aeZFLwk?filter=hot&root_comment_id=0&type=comment'

dr.get(url)
dr.add_cookie(cookies)
time.sleep(10)

# js="var q=document.getElementById('id').scrollTop=10000"
# driver.execute_script(js)
#
#
# while True:
#     scroll(dr)
#     try:
#         dr.find_element_by_xpath(
#             '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[4]/div/div[2]/div[2]/div/div/a').click()
#     except NoSuchElementException:
#         print("No such element")
#     time.sleep(4)
# NoSuchElementException
# by xpath
# xpath
# dr.find_element_by_xpath('/html/body/form/div[3]/div/label/input').click()

# 退出
# close方法关闭当前的浏览器窗口，
# quit方法不仅关闭窗口，还会彻底的退出 webdriver，
# 释放与driver server之间的连接。
# 所以简单来说quit是更加彻底的 close，
# quit会更好的释放资源，适合强迫症和完美主义者


# dr.quit()


# (<class 'selenium.common.exceptions.NoSuchElementException'>, NoSuchElementException('no such element: Unable to locate element: {"method":"link text","selector":"查看更多"}\n  (Session info: chrome=81.0.4044.138)', None, None), <traceback object at 0x00000201C73E5348>)
