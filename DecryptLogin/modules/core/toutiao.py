'''
Function:
    今日头条模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
import re
import os
import time
import base64
import requests
from ..utils import removeImage, saveImage, showImage


'''PC端登录今日头条'''
class toutiaoPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in toutiao in pc mode'


'''移动端登录今日头条'''
class toutiaoMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in toutiao in mobile mode'


'''扫码登录今日头条'''
class toutiaoScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in toutiao in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 下载二维码
        params = {
            'service': 'https://www.toutiao.com',
            'need_logo': 'false',
            'aid': '24',
            'account_sdk_source': 'sso',
            'language': 'zh',
        }
        response = self.session.get(self.getqrcode_url, params=params)
        response_json = response.json()
        token = response_json['data']['token']
        qrcode = base64.b64decode(response_json['data']['qrcode'])
        saveImage(qrcode, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检查二维码状态
        while True:
            params = {
                'service': 'https://www.toutiao.com',
                'token': token,
                'need_logo': 'false',
                'aid': '24',
                'account_sdk_source': 'sso',
                'language': 'zh',
            }
            response = self.session.get(self.check_url, params=params)
            response_json = response.json()
            if response_json['data']['status'] in ['1', '2']:
                time.sleep(1)
                continue
            elif response_json['data']['status'] in ['3']:
                break
            else:
                raise RuntimeError(response_json)
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        infos_return = response_json
        redirect_url = response_json['data']['redirect_url']
        response = self.session.get(redirect_url)
        response = self.session.get(self.token_url)
        infos_return['token_info'] = response.json()
        username = response.json()['data']['token']
        print('[INFO]: Account -> %s, login successfully' % username)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
        self.getqrcode_url = 'https://sso.toutiao.com/get_qrcode/'
        self.check_url = 'https://sso.toutiao.com/check_qrconnect/'
        self.token_url = 'https://www.toutiao.com/tt-anti-token'
        self.session.headers.update(self.headers)


'''
Function:
    今日头条模拟登录
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
class toutiao():
    def __init__(self, **kwargs):
        self.info = 'login in toutiao'
        self.supported_modes = {
            'pc': toutiaoPC(**kwargs),
            'mobile': toutiaoMobile(**kwargs),
            'scanqr': toutiaoScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in toutiao.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in toutiao.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)