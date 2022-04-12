import requests
import json
import time
import re
import os


class run:
    def __init__(self):  # 初始化变量
        self.url_bv = 'https://api.bilibili.com/x/space/arc/search?mid=%s&ps=30&tid=0&pn=%s&keyword=&order=pubdate&jsonp=jsonp'
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'}
        self.bv_url_list = []

    def bvid(self, url):  # 获取视频bv号
        text = requests.get(url, headers=self.header).text
        time.sleep(1)
        text = json.loads(text)
        text_list = text['data']['list']['vlist']
        for text in text_list:
            bvid = text['bvid']
            self.bv_url_list.append('https://www.bilibili.com/video/' + bvid)
            print(bvid)
        print('*'*50)

    def video(self, level):  # 获得视频下载链接
        if not os.path.exists('download'):
            os.mkdir('download')
            print('已创建文件夹')

        for bv_url in self.bv_url_list:
            param = {'url': bv_url}
            url_text = json.loads(requests.get('http://118.24.49.88/Video/X.php', headers=self.header, params=param).text)
            time.sleep(2)
            name = url_text['name'].split('@')[0]
            url_list = re.findall("'url': '""(.*?)""'", str(url_text))

            if level == '1':
                url = url_list[0]
                self.download_image(name, url)

            elif level == '2':
                url = url_list[1]
                self.download_video(name, url)

            elif level == '3':
                url = url_list[2]
                self.download_video(name, url)

            else:
                print('%s不是有效数字' % level)
                exit()

    def download_image(self, name, url):  # 负责图片下载
        print('正在下载{name}')
        with open(r'./download/%s.jpg' % name, 'wb') as image:
            image.write(requests.get(url, headers=self.header).content)
            print('%s.jpg下载完成' % name)

    def download_video(self, name, url):  # 负责视频下载
        print('正在下载{name}')
        with open(r'./download/%s.mp4' % name, 'wb') as video:
            video.write(requests.get(url, headers=self.header).content)
            print('%s.mp4下载完成' % name)

    def main(self, uid, number, level):
        for num in range(1, int(number)+1):
            self.bvid(self.url_bv % (uid, num))
        self.video(level)


if __name__ == '__main__':
    r = run()
    uid = input('输入up主的uid\n')
    level = input('1.下载封面\n2.流畅视频\n3.高清视频\n输入数字____\n')
    num = input('爬几页?\n')
    print('速度很慢，请耐心等待')
    r.main(uid, num, level)
