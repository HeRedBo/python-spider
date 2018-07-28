# -*- coding:UTF-8 -*-

import os
import time
import requests
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


class DoubanSpider(object):

    def __init__(self):
        self.request_urls = []
        self.douban_top250_url = "https://movie.douban.com/top250?start=%s&filter="

        if 'top250_images' not in os.listdir('.'):
            os.mkdir('top250_images')
        self.path = os.path.join(os.path.abspath('.'), 'top250_images')
        os.chdir(self.path)

    def run(self):

        for i in range(1, 11):
            self.request_urls.append(self.douban_top250_url % (25 * (i-1)))
        start_time = time.time()
        print('**' * 25)
        # 利用并发下载电影图片
        executor = ThreadPoolExecutor(max_workers=15)  # 可以自己调整max_workers,即线程的个数
        # submit()的参数： 第一个为函数， 之后为该函数的传入参数，允许有多个
        future_tasks = [executor.submit(self.download_picture, url) for url in self.request_urls]
        # 等待所有的线程完成，才进入后续的执行
        wait(future_tasks, return_when=ALL_COMPLETED)
        end_time = time.time()
        print(self.path)
        print('使用多线程 程序运行耗时 %s秒', (end_time - start_time))
        print('**' * 25)
        
    def download_picture(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('div', class_="article")
        images = content.find_all('img')
        picture_name_list = [image['alt'] for image in images]
        picture_link_list = [image['src'] for image in images]
        # 利用urllib.request..urlretrieve正式下载图片
        for picture_name, picture_link in zip(picture_name_list, picture_link_list):
            urllib.request.urlretrieve(picture_link, self.path + '/%s.jpeg' % picture_name)
            print("%s 电影海报图片下载成功" % picture_name)


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.run()
