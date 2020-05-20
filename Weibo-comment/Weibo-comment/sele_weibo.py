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


# 打开浏览器
dr = webdriver.Chrome()
# 最大化浏览器
dr.maximize_window()
# 设置大小
url = 'https://weibo.com/3165034955/J1aeZFLwk?filter=hot&root_comment_id=0&type=comment'

dr.get(url)
time.sleep(3)

while True:
    scroll(dr)
    try:
        dr.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[4]/div/div[2]/div[2]/div/div/a').click()
    except NoSuchElementException:
        print("No such element")
    time.sleep(2)

# 退出
# close方法关闭当前的浏览器窗口，
# quit方法不仅关闭窗口，还会彻底的退出 webdriver，
# 释放与driver server之间的连接。
# 所以简单来说quit是更加彻底的 close，
# quit会更好的释放资源，适合强迫症和完美主义者


# dr.quit()


# (<class 'selenium.common.exceptions.NoSuchElementException'>, NoSuchElementException('no such element: Unable to locate element: {"method":"link text","selector":"查看更多"}\n  (Session info: chrome=81.0.4044.138)', None, None), <traceback object at 0x00000201C73E5348>)
