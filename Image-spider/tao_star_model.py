# -*- coding:UTF-8 -*-

import os
import threading
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TaoStartModelSpider(object):

    def __init__(self):
        self.homePage = 'https://mm.taobao.com/search_tstar_model.htm?'
        self.outputDir = 'photo/'
        self.parser = 'html5lib'
        self.driver = None
        self.get_driver()
        self.girls_info = []

    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self. driver = webdriver.Chrome(chrome_options=chrome_options)

    def run(self):
        self.get_girls_list()
        if self.girls_info:
            self.save_girls_info()
        else:
            print('error')

        # 抓取完毕需要将 driver 关闭
        self.driver.close()

    def save_girls_info(self):

        for girl_NL, girl_HW, girl_HURl, girl_cover in self.girls_info:
            print("[*]Girl :", girl_NL, girl_HW)
            # 为妹子建立文件夹
            self.my_mkdir(self.outputDir + girl_NL)
            print("[*]saving...")
            data = urlopen(girl_cover).read()

            with open(self.outputDir + girl_NL + '/cover.jpg', 'wb') as f:
                f.write(data)
            print("[+]loading Cover...")
            self.get_images(girl_HURl, self.outputDir + girl_NL)

    def get_girls_list(self):
        self.driver.get(self.homePage)  # 获取目标网页地址
        bsObj = BeautifulSoup(self.driver.page_source, self.parser)
        print("[*]OK GET PAGE")
        girls_list = self.driver.find_element_by_id("J_GirlsList").text.split("\n")  # 获取主页上所有妹子的姓名，所在城市，身高、体重等信息

        images_url = re.findall('\/\/gtd\.alicdn\.com\/sns_logo.*\.jpg', self.driver.page_source)  # 获取所有妹子的封面图片

        girls_url = bsObj.find_all("a", {"href": re.compile("\/\/.*\.htm\?(userId=)\d*")})
        girls_NL = girls_list[::3]  # 列表切片
        girls_HW = girls_list[1::3]
        girls_HURl = [('http:' + i['href']) for i in girls_url]
        girls_photo_URL = [('https:' + i) for i in images_url]
        self.girls_info = zip(girls_NL, girls_HW, girls_HURl, girls_photo_URL)

    def get_images(self, url, path):

        self.driver.get(url)
        print("[*]Opening...")
        bsObj = BeautifulSoup(self.driver.page_source, self.parser)

        # 获取模特个人主页上的艺术照地址
        images = bsObj.find_all("img", {"src": re.compile(".*\.jpg")})
        for i, img in enumerate(images[1::]):  # 不包含与封面图片一样的头像
            try:
                html = urlopen('https:' + img['src'])
                data = html.read()
                file_name = "{}/{}.jpg".format(path, i+1)
                print("[+]Loading...", file_name)
                with open(file_name, 'wb') as f:
                    f.write(data)

            except Exception:
                print("[!]Address Error!")

    def my_mkdir(self, path):

        dirs = path.split("/")
        dir_name = ''
        for dir in dirs:
            dir_name += dir + '/'
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
                print("[*]新建文件夹", dir_name)


spider = TaoStartModelSpider()
spider.run()
