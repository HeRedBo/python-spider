# -*- coding:UTF-8 -*-
import requests, json
if __name__ == '__main__':
    target = 'http://unsplash.com/napi/feeds/home'
    headers = {'authorization': '72664f05b2aee9ed032f9f4084f0ab55aafe02704f8b7f8ef9e28acbec372d09'}
    req = requests.get(url=target, headers=headers, verify=False)
    html = json.loads(req.text)
    print(html)
    next_page = html['next_page']
    print('下一页地址:', next_page)
    for each in html['photos']:
        print('图片ID:', each['id'])



