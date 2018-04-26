# -*- coding:UTF-8 -*-
import requests, json, time, sys
from contextlib import closing

class PhotoSpider(object):

    def __init__(self):
        self.photos_id = []
        self.download_server = 'https://unsplash.com/photos/xxx/download?force=trues'
        self.target = "https://unsplash.com/napi/feeds/home"
        self.headers = {'authorization': 'Client-ID 72664f05b2aee9ed032f9f4084f0ab55aafe02704f8b7f8ef9e28acbec372d09'}

    def get_ids(self):
        """
        获取图片的ID
        :return:
        """
        req = requests.get(url=self.target, headers=self.headers, verify=False)
        html = json.loads(req.text)

        next_page = html['next_page']
        for each in html['photos']:
            self.photos_id.append(each['id'])

        print(next_page)
        time.sleep(2)
        for i in range(2):
            req = requests.get(url=next_page, headers=self.headers, verify=False)
            html = json.loads(req.text)
            print('html')
            print(html)
            next_page = html['next_page']
            for each in html['photos']:
                self.photos_id.append(each['id'])
            time.sleep(1)

    def download(self, photo_id, file_name):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3'}
        target = self.download_server.replace('xxx', photo_id)
        with closing(requests.get(url=target, stream=True, verify=False, headers=self.headers)) as r:
            with open("&d.jpg" % file_name, 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        

if __name__ == '__main__':
    gp = PhotoSpider()
    print("获取图片链接中:")
    gp.get_ids()
    print("图片下载中：")
    for i in range(len(gp.photos_id)):
        print(" 正在下载第%d张图片" % (i + 1))
        gp.download(gp.photos_id[i], (i + 1))