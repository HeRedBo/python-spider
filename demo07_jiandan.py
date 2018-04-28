# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import hashlib
import re
import base64
import threading
import multiprocessing
import time


def _md5(value):
    """
    MD5加密
    :param value:string 需要加密的字符串
    :return:
    """
    m = hashlib.md5()
    m.update(value.encode('utf-8'))
    return m.hexdigest()


def _base64_decode(data):
    """
    base64转码 要注意原字符串长度报错问题
    :param data: string
    :return:
    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.b64decode(data)


def get_image_url(m, r='', d=0):
    """
    解密获取图片链接地址
    :param m:
    :param r:
    :param d:
    :return:
    """
    e = 'DECODE'
    q = 4
    r = _md5(r)
    o = _md5(r[0:0 + 16])
    n = _md5(r[16:16 + 16])
    l = m[0:q]

    c = o + _md5(o + l)
    m = m[q:]

    k = _base64_decode(m)
    h = list(range(256))
    b = [ord(c[g % len(c)]) for g in range(256)]

    f = 0
    for g in range(0, 256):
        f = (f + h[g] + b[g]) % 256
        tmp = h[g]
        h[g] = h[f]
        h[f] = tmp

    t = ""
    p, f = 0, 0
    for g in range(0, len(k)):
        p = (p + 1) % 256
        f = (f + h[p]) % 256
        tmp = h[p]
        h[p] = h[f]
        h[f] = tmp
        t += chr(k[g] ^ (h[(h[p] + h[f]) % 256]))
    t = t[26:]
    return t


def get_r(js_url):
    """获取关键字符串"""
    js = requests.get(js_url).text
    _r = re.findall('c=[\w\d]+\(e,"(.*?)"\)', js)[0]
    return _r
    # ;var c=jdrsHdRQYUtzgNIRZi4OecCAhMq7y2DMJ5(e,"k7zymzBcxHyuRsVSlnZ7R35EEvA4ka0E")


def get_urls(url):
    """
    获取一个页面的所有图片地址
    :param url:
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'jandan.net'
    }

    html = requests.get(url, headers=headers).text
    js_url = 'http:' + re.findall('<script src="(//cdn.jandan.net/static/min/[\w\d]+\.\d+\.js)"></script>', html)[-1]
    _r = get_r(js_url)

    soup = BeautifulSoup(html, 'lxml')
    tags = soup.select('.img-hash')

    for tag in tags:
        img_hash = tag.text
        img_url = get_image_url(img_hash, _r)
        print(img_url)


def load_img(img_url, path):
    """
    下载单张图片到定制文件夹中
    :param img_url:string 图片链接地址
    :param path:string 保存的目录文件中
    :return:
    """
    name = img_url.split("/")[-1]
    file_name = "{}\\{}".format(path, name)
    item = requests.get(img_url).content
    with open(file_name, 'wb') as f:
        f.write(item)
    print("{} is loaded".format(name))


def load_images(url, path):
    """
    多线程下载单页图片
    :param url:
    :param path:
    :return:
    """
    threads = []

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'jandan.net'
    }

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    js_url = 'http:' + re.findall('<script src="(//cdn.jandan.net/static/min/[\w\d]+\.\d+\.js)"></script>', html)[-1]
    _r = get_r(js_url)


    # 这个地方必须使用[-1]来提取js地址，因为有的页面有两个js地址，其中第一个是被注释了不用的
    js_url = re.findall('<script src="(//cdn.jandan.net/static/min/[\w\d]+\.\d+\.js)"></script>', html)[-1]
    _r = get_r('http:{}'.format(js_url))

    tags = soup.select('.img-hash')
    for tag in tags:
        img_hash = tag.text
        img_url = 'http:' + get_image_url(img_hash, _r)
        t = threading.Thread(target=load_img, args=(img_url, path))
        threads.append(t)

    for i in threads:
        i.start()
    for i in threads:
        i.join()
    print(url, 'is ok')


def main(start, end, path):

    pool = multiprocessing.Pool(processes=2)
    base_url = 'http://jandan.net/ooxx/page-{}'
    for i in range(start, end+1):
        url = base_url.format(i)
        pool.apply_async(func=load_images, args=(url, path))
    pool.close()
    pool.join()


if __name__ == '__main__':
    t = time.time()
    main(50, 70, r'./jiandan_images')
    print(time.time() - t)