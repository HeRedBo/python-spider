# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
import time


class ShuaiaSpider(object):
    """
    http://www.shuaia.net 网站图片爬取spider
    """
    def __init__(self):
        self.target = 'http://www.shuaia.net/jirounan/'
        self.target_host = 'http://www.shuaia.net/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        self.list_url = []
        self.spider_page_count = 2  # 抓取的页面数量
        self.encoding = 'utf-8'
        self.image_dir = 'shuaia_images'

    def run(self):
        self.__say_hello()
        self.get_images()
        if self.list_url:
            self.download_images()
        else:
            print("未搜索到相关图片信息")

    def get_images(self):
        """
        获取远端图片
        :return:
        """
        for num in range(1, self.spider_page_count):
            if num == 1:
                url = self.target + 'index.html'
            else:
                url = self.target + 'index_%d.html'
                url = url % num
            req = requests.get(url=url, headers=self.headers)
            req.encoding = 'utf-8'
            html = req.text
            bf = BeautifulSoup(html,'lxml')
            targets_url = bf.find_all(class_='item-img')
            for each in targets_url:
                self.list_url.append(each.img.get('alt') + '=' + each.get('href'))
        print('连接采集完成')

    def download_images(self):
        print("图片开始下载...")
        for each_img in self.list_url:
            img_info = each_img.split('=')
            target_url = img_info[1]
            filename = img_info[0] + '.jpg'
            print('下载：' + filename)
            img_req = requests.get(url=target_url, headers=self.headers)
            img_req.encoding = self.encoding
            img_html = img_req.text
            img_bf_1 = BeautifulSoup(img_html, 'lxml')
            img_url = img_bf_1.find_all('div', class_='wr-single-content-list')
            img_bf_2 = BeautifulSoup(str(img_url), 'lxml')
            img_url = self.target_host + img_bf_2.div.img.get('src')
            self.download(img_url, filename)
            time.sleep(1)
        print("图片下载完成...")

    def __say_hello(self):
        print('*' * 100)
        print('\t\t\t\thttp://www.shuaia.net 网页图片爬虫')
        print('*' * 100)

    def download(self, img_url, file_name):
        img_dir = self.image_dir
        if img_dir not in os.listdir():
            os.makedirs(img_dir)
        filename = img_dir + "/" + file_name
        urlretrieve(url=img_url, filename=filename)


if __name__ == '__main__':
    spider = ShuaiaSpider()
    spider.run()
