# -*- coding:UTF-8 -*-
import requests, sys
from bs4 import BeautifulSoup

"""
类说明： 下载《笔趣看》网小说《一年永恒》
"""


class BiqukanSpider(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数

    """
    函数说明：获取下载链接
    
    """
    def get_download_url(self):
        req = requests.get(url=self.target)
        html = req.text
        div_bf = BeautifulSoup(html, "html.parser")
        div = div_bf.find_all("div", class_="listmain")
        a_bf = BeautifulSoup(str(div[0]), "html.parser")
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get("href"))

    def get_contents(self, target):
        """
        获取章节内容
        :param target:string 下载链接
        :return:text  章节内容
        """
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, "html.parser")
        texts = bf.find_all('div', class_="showtxt")
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    def writer(self, name, path, text):
        """
        将爬取道德文章内容写入文件中
        :param name:string 文章章节名称
        :param path: string 小说保存名称
        :param text:string 章节内容
        :return: 无
        """
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write("\n\n")


if __name__ == '__main__':
    spider = BiqukanSpider()
    spider.get_download_url()
    print("《一念永恒》开始下载：")

    for i in range(spider.nums):
        spider.writer(spider.names[0], "一年永恒.txt", spider.get_contents(spider.urls[i]))
        sys.stdout.write("已下载 %.3f%%" % float(i/spider.nums) + '\r')
        sys.stdout.flush()

    print("《一念永恒》下载完成")

