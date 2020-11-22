'''
Function:
    人人网模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import os
import re
import random
import requests
from ..utils.misc import *


'''PC端登录人人网'''
class renrenPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in renren in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 判断是否需要验证码
        is_need_captcha = False
        response = self.session.get(self.home_url)
        if 'id="verifyPic_login"' in response.text:
            is_need_captcha = True
        # 如果需要验证码, 则获取验证码
        if is_need_captcha:
            response = self.session.get(self.captcha_url.format(random.random()))
            saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
            if crack_captcha_func is None:
                showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                captcha = input('Input the captcha: ')
            else:
                captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
            removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
        # 进行登录
        data = {
            'email': username,
            'origURL': 'http://www.renren.com/home',
            'domain': 'renren.com',
            'key_id': 1,
            'captcha_type': 'web_login',
            'password': password,
            'f': ''
        }
        if is_need_captcha: data.update({'icode': captcha})
        response = self.session.post(self.login_url, data=data)
        user_id = re.findall(r'id:"(.*?)",', response.text.replace('\n', '').replace(' ', ''))
        user_ruid = re.findall(r'ruid:"(.*?)",', response.text.replace('\n', '').replace(' ', ''))
        name = re.findall(r'name:"(.*?)",', response.text.replace('\n', '').replace(' ', ''))
        privacy = re.findall(r'privacy:"(.*?)",', response.text.replace('\n', '').replace(' ', ''))
        request_token = re.findall(r"requestToken:'(.*?)',", response.text.replace('\n', '').replace(' ', ''))
        _rtk = re.findall(r"_rtk:'(.*?)'}", response.text.replace('\n', '').replace(' ', ''))
        is_vip = re.findall(r'user.isvip=(.*?);', response.text.replace('\n', '').replace(' ', ''))
        # 登录失败(一般就是账户或密码错误)
        if (not name[0]) and (u'不匹配' in response.text):
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 登录成功
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {
            'username': username, 
            'id': user_id[0], 
            'ruid': user_ruid[0], 
            'name': name[0], 
            'privacy': privacy[0], 
            'requestToken': request_token[0],
            '_rtk': _rtk[0], 
            'isvip': is_vip[0]
        }
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        self.home_url = 'http://renren.com/'
        self.login_url = 'http://www.renren.com/PLogin.do'
        self.captcha_url = 'http://icode.renren.com/getcode.do?t=web_login&rnd={}'
        self.session.headers.update(self.headers)


'''移动端登录人人网'''
class renrenMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in renren in mobile mode'


'''扫码登录人人网'''
class renrenScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in renren in scanqr mode'


'''
Function:
    人人网模拟登录
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
class renren():
    def __init__(self, **kwargs):
        self.info = 'login in renren'
        self.supported_modes = {
            'pc': renrenPC(**kwargs),
            'mobile': renrenMobile(**kwargs),
            'scanqr': renrenScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in renren.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in renren.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)