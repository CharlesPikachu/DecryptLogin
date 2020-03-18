'''
Function:
    大吼一声发条微博
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import random
import struct
import pyaudio
import argparse
from DecryptLogin import login


'''命令行参数解析'''
def parseArgs():
    parser = argparse.ArgumentParser(description='大吼一声发条微博')
    parser.add_argument('--username', dest='username', help='用户名', type=str, required=True)
    parser.add_argument('--password', dest='password', help='密码', type=str, required=True)
    args = parser.parse_args()
    return args


'''自动发微博'''
class WeiboSender():
    def __init__(self, username, password, **kwargs):
        self.nickname, self.uid, self.session = WeiboSender.login(username, password)
        self.headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
                        }
    '''外部调用'''
    def start(self):
        while True:
            # 输入微博路径
            weibopath = input('请输入想要发送的微博路径(例如: ./weibo, 里面的weibo.md文件里写微博内容, pictures文件夹里放配图) ——> ')
            # 解析微博
            text, pictures = self.__parseWeibo(weibopath)
            # 大吼一声确定是该微博
            print('微博内容为: %s\n配图数量为: %s' % (text, len(pictures)))
            print('如果您确认想发这条微博, 请在30s内对着电脑大吼一声')
            stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, 
                                            channels=1, 
                                            rate=int(pyaudio.PyAudio().get_device_info_by_index(0)['defaultSampleRate']), 
                                            input=True, 
                                            frames_per_buffer=1024)
            is_send_flag = False
            start_t = time.time()
            while True:
                time.sleep(0.1)
                audio_data = stream.read(1024)
                k = max(struct.unpack('1024h', audio_data))
                # --声音足够大, 发送这条微博
                if k > 8000:
                    is_send_flag = True
                    break
                # --时间到了还没有足够大的声音, 不发这条微博
                if (time.time() - start_t) > 30:
                    break
            # 发送微博
            if is_send_flag:
                print('大吼成功! 准备开始发送该条微博~')
                if self.__sendWeibo(text, pictures):
                    print('[INFO]: 微博发送成功!')
    '''发微博'''
    def __sendWeibo(self, text, pictures):
        # 上传图片
        pic_id = []
        url = 'https://picupload.weibo.com/interface/pic_upload.php'
        params = {
                    'data': '1',
                    'p': '1',
                    'url': 'weibo.com/u/%s' % self.uid,
                    'markpos': '1',
                    'logo': '1',
                    'nick': '@%s' % self.nickname,
                    'marks': '1',
                    'app': 'miniblog',
                    's': 'json',
                    'pri': 'null',
                    'file_source': '1'
                }
        for picture in pictures:
            res = self.session.post(url, headers=self.headers, params=params, data=picture)
            res_json = res.json()
            if res_json['code'] == 'A00006':
                pid = res_json['data']['pics']['pic_1']['pid']
                pic_id.append(pid)
            time.sleep(random.random()+0.5)
        # 发微博
        url = 'https://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        data = {
                    'title': '',
                    'location': 'v6_content_home',
                    'text': text,
                    'appkey': '',
                    'style_type': '1',
                    'pic_id': '|'.join(pic_id),
                    'tid': '',
                    'pdetail': '',
                    'mid': '',
                    'isReEdit': 'false',
                    'gif_ids': '',
                    'rank': '0',
                    'rankid': '',
                    'pub_source': 'page_2',
                    'topic_id': '',
                    'updata_img_num': str(len(pictures)),
                    'pub_type': 'dialog'
                }
        headers = self.headers.copy()
        headers.update({'Referer': 'http://www.weibo.com/u/%s/home?wvr=5' % self.uid})
        res = self.session.post(url, headers=headers, data=data)
        is_success = False
        if res.status_code == 200:
            is_success = True
        return is_success
    '''待发送微博内容解析'''
    def __parseWeibo(self, weibopath):
        text = open(os.path.join(weibopath, 'weibo.md'), 'r', encoding='utf-8').read()
        pictures = []
        for filename in sorted(os.listdir(os.path.join(weibopath, 'pictures'))):
            if filename.split('.')[-1].lower() in ['jpg', 'png']:
                pictures.append(open(os.path.join(weibopath, 'pictures', filename), 'rb').read())
        if len(pictures) > 9:
            print('[Warning]: 一条微博最多只能有9张配图, 程序现在将自动剔除多出的图片')
            pictures = pictures[:9]
        return text, pictures
    '''利用DecryptLogin模拟登录'''
    @staticmethod
    def login(username, password):
        lg = login.Login()
        infos_return, session = lg.weibo(username, password, 'pc')
        return infos_return.get('nick'), infos_return.get('uid'), session
    

'''run'''
if __name__ == '__main__':
    args = parseArgs()
    sender = WeiboSender(args.username, args.password)
    sender.start()