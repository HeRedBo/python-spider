# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    target = 'http://www.biqukan.com/1_1094/'
    server = 'http://www.biqukan.com'
    req = requests.get(url=target)
    html = req.text
    div_bf = BeautifulSoup(html, "html.parser")
    div = div_bf.find_all('div', class_='listmain')
    a_bf = BeautifulSoup(str(div[0]), "html.parser")
    a = a_bf.find_all("a")
    for each in a:
        print(each.string, server + each.get("href"))
    # print(texts[0].text.replace('\xa0' * 8, '\n\n'))
