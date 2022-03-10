'''
Function:
    中关村在线模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-30
'''
import os
import re
import time
import requests
from hashlib import md5
from ..utils.misc import *


'''PC端登录中关村在线'''
class zgconlinePC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zgconline in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 请求home_url
        self.session.get(self.home_url)
        # 请求login_url
        data = {
            'userid': username,
            'pwd': md5((password+'zol').encode(encoding='utf-8')).hexdigest(),
            'is_auto': '1',
            'backUrl': 'http://www.zol.com.cn/'
        }
        cookies = {'ip_ck': self.__getIPCK()}
        self.session.headers.update({'Content-type': 'application/x-www-form-urlencoded'})
        response = self.session.post(self.login_url, data=data, cookies=cookies)
        response_json = response.json()
        # 登录成功
        if response_json.get('info') == 'ok':
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号或密码有误
        elif response_json.get('info') == 'error' and response_json.get('msg') == '账号或密码错误,请重试':
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 需要验证码
        elif response_json.get('info') == 'error' and response_json.get('ext', ''):
            imgcode = str(int(time.time() * 1000))
            captcha_url = 'http://service.zol.com.cn/group/auth_code.php?t=%s' % imgcode
            response = self.session.get(captcha_url)
            saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
            if crack_captcha_func is None:
                showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                captcha = input('Input the captcha: ')
            else:
                captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
            removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
            data = {
                'act': 'checking',
                'userid': username,
                'backurl': re.findall(r'backurl=(.*?)', response_json['ext'])[0],
                'checkcode': re.findall(r'checkcode=(.*?)&', response_json['ext'])[0],
                'door': captcha,
                'imgcode': imgcode,
            }
            response = self.session.post(response_json['ext'], data=data)
            self.login(username, password, crack_captcha_func, **kwargs)
        # 其他原因
        else:
            raise RuntimeError(response_json.get('msg'))
    '''获得ipck'''
    def __getIPCK(self):
        response = self.session.get(self.ipck_url.format(int(time.time()/1000), ''))
        return response.json().get('ipck')
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Referer': 'http://service.zol.com.cn/user/login.php?backUrl=http://www.zol.com.cn/',
            'Origin': 'http://service.zol.com.cn'
        }
        self.home_url = 'http://www.zol.com.cn/'
        self.login_url = 'http://service.zol.com.cn/user/ajax/login2014/login.php'
        self.ipck_url = 'http://js.zol.com.cn/pvn/pv.ht?&t={}&c={}'
        self.session.headers.update(self.headers)


'''移动端登录中关村在线'''
class zgconlineMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zgconline in mobile mode'


'''扫码登录中关村在线'''
class zgconlineScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zgconline in scanqr mode'


'''
Function:
    中关村在线模拟登录
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
class zgconline():
    def __init__(self, **kwargs):
        self.info = 'login in zgconline'
        self.supported_modes = {
            'pc': zgconlinePC(**kwargs),
            'mobile': zgconlineMobile(**kwargs),
            'scanqr': zgconlineScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in zgconline.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in zgconline.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)