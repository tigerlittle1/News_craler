from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import threading


class Crawker():

    def __init__(self,URL='https://anewstip.com/search/tweets/?q=artificial+intelligence'):
        chrome_options = webdriver.ChromeOptions()
        # 添加 User-Agent
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"')
        # 指定瀏覽器解析度
        chrome_options.add_argument('window-size=1920x1080')
        # 不載入圖片，提升速度
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        # 瀏覽器不提供視覺化頁面
        chrome_options.add_argument('--headless')
        # 禁用 JavaScript
        chrome_options.add_argument("--disable-javascript")
        # 禁用瀏覽器彈出視窗
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            }
        }
        chrome_options.add_experimental_option('prefs', prefs)

        self.driver = Chrome(options=chrome_options)
        # 存取 Website
        self.driver.get(URL)

    def get_soup(self):
        # 取得網頁原始碼
        html = self.driver.page_source
        # 解析下一頁的 html
        soup = BeautifulSoup(html, 'html.parser')
        return soup

class Crawker_Thread(threading.Thread):
    def __init__(self, target=None, args=(), **kwargs):
        super(Crawker_Thread, self).__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self.__result__ = None

    def run(self):
        if self._target == None:
            return
        self.__result__ = self._target(self._args)

    def get_result(self):
        self.join()#當需要取得結果值的時候阻塞等待子執行緒完成
        return self.__result__

