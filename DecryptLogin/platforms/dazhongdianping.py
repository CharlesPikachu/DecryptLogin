'''
Function:
    大众点评模拟登录
        --PC端: http://www.dianping.com/
        --移动端暂不支持
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
更新日期:
    2020-07-24
'''
import os
import re
import time
import random
import requests
from ..utils.misc import *


'''
Function:
    大众点评模拟登录
Detail:
    -login:
        Input:
            --username: 用户名
            --password: 密码
            --mode: mobile/pc
            --crackvcFunc: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
            --proxies: 为requests.Session()设置代理
        Return:
            --infos_return: 用户名等信息
            --session: 登录后的requests.Session()
'''
class dazhongdianping():
    def __init__(self, **kwargs):
        self.info = 'dazhongdianping'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
    '''登录函数'''
    def login(self, username='', password='', mode='pc', crackvcFunc=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 移动端接口
        if mode == 'mobile':
            raise NotImplementedError
        # PC端接口
        elif mode == 'pc':
            self.__initializePC()
            self.session.get(self.home_url)
            # 获取二维码
            response = self.session.get(self.getqrcodeimg_url+str(random.random()), headers=self.qr_headers)
            saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
            showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
            # 检测二维码状态
            lgtoken = self.session.cookies.get('lgtoken')
            while True:
                response = self.session.post(self.queryqrcodestatus_url, data={'lgtoken': lgtoken}, headers=self.status_headers)
                response_json = response.json()
                # --扫码成功
                if response_json['msg']['status'] in [2]:
                    response = self.session.get(self.home_url, headers=self.headers)
                    username = re.findall(r"'userName':.*?'(.*?)',", response.text)
                    username = username[0] if username else 'fail to extract username'
                    userid = re.findall(r"'userId':.*?'(.*?)',", response.text)
                    userid = userid[0] if userid else 'fail to extract userid'
                    break
                # --二维码已经失效
                elif response_json['msg']['status'] in [-1]:
                    raise RuntimeError('Fail to login, qrcode has expired...')
                # --正在扫码或其他原因
                elif response_json['msg']['status'] in [0, 1]:
                    pass
                time.sleep(0.5)
            # 登录成功
            removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
            print('[INFO]: Account -> %s, login successfully...' % username)
            infos_return = {'username': username, 'userid': userid}
            return infos_return, self.session
        # mode输入有误
        else:
            raise ValueError('Unsupport argument in dazhongdianping.login -> mode %s, expect <mobile> or <pc>...' % mode)
    '''初始化PC端'''
    def __initializePC(self):
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                    }
        self.status_headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                                'Accept':'*/*',
                                'Accept-Encoding':'gzip, deflate, br',
                                'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                            }
        self.qr_headers = {
                            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
                        }
        self.home_url = 'http://www.dianping.com/'
        self.getqrcodeimg_url = 'https://account.dianping.com/account/getqrcodeimg?'
        self.queryqrcodestatus_url = 'https://account.dianping.com/account/ajax/queryqrcodestatus'
    '''初始化移动端'''
    def __initializeMobile(self):
        pass


'''test'''
if __name__ == '__main__':
    dazhongdianping().login()