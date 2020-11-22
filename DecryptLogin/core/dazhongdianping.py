'''
Function:
    大众点评模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import os
import re
import time
import random
import requests
from ..utils.misc import *


'''PC端登录大众点评'''
class dazhongdianpingPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in dazhongdianping in pc mode'


'''移动端登录大众点评'''
class dazhongdianpingMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in dazhongdianping in mobile mode'


'''扫码登录大众点评'''
class dazhongdianpingScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in dazhongdianping in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化cookies
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
                raise RuntimeError('Fail to login, qrcode has expired')
            # --正在扫码或其他原因
            elif response_json['msg']['status'] in [0, 1]:
                pass
            time.sleep(0.5)
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username, 'userid': userid}
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
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


'''
Function:
    大众点评模拟登录
Detail:
    -login:
        Input:
            --username: 用户名
            --password: 密码
            --mode: mobile/pc/scanqr
            --crack_captcha_func: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
            --proxies: 为requests.Session()设置代理
        Return:
            --infos_return: 用户名等信息
            --session: 登录后的requests.Session()
'''
class dazhongdianping():
    def __init__(self, **kwargs):
        self.info = 'login in dazhongdianping'
        self.supported_modes = {
            'pc': dazhongdianpingPC(**kwargs),
            'mobile': dazhongdianpingMobile(**kwargs),
            'scanqr': dazhongdianpingScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in dazhongdianping.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in dazhongdianping.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)