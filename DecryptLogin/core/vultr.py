'''
Function:
    Vultr模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import re
import os
import requests
from hashlib import md5
from ..utils.misc import *


'''PC端登录Vultr'''
class vultrPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in vultr in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化cookies
        response = self.session.get(self.vultr_url)
        # 看看是否需要输入验证码(不支持处理谷歌的点击验证码)
        is_need_captcha = False
        s = re.findall(r'captcha\.php\?s=(.*?)"', response.text)
        action = re.findall(r'name="action" value="(.*?)"', response.text)[0]
        if s:
            s = s[0]
            is_need_captcha = True
        if is_need_captcha:
            response = self.session.get(self.captcha_url.format(s))
            saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
            if crack_captcha_func is None:
                showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                captcha = input('Input the captcha: ')
            else:
                captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
            removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
        # 模拟登录
        data = {
            'action': action,
            'login_type': 'normal',
            'token': self.__calcToken(action),
            'username': username,
            'password': password
        }
        if is_need_captcha:
            data['captcha'] = captcha
        response = self.session.post(self.vultr_url, data=data, headers=self.login_headers)
        # 登录成功
        if 'Hello' in response.text:
            name = re.findall(r'Hello, (.*?)!', response.text)[0]
            infos_return = {'username': username, 'name': name}
            print('[INFO]: Account -> %s, login successfully' % username)
            return infos_return, self.session
        # 登录失败, 如果网络可以访问谷歌, 很可能是因为出现了谷歌的点击验证码而登录失败, 而非账户/密码/验证码输入错误
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password or captcha error. Noted, if your network could visit google.com, maybe you are detected as a robot rather than username or password error' % username)
    '''计算token'''
    def __calcToken(self, action):
        token = 0
        while True:
            action_hash = md5((action + str(token)).encode(encoding='utf-8')).hexdigest()
            if action_hash[:2] == '00':
                break
            token += 1
        return str(token)
    '''初始化'''
    def __initialize(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        self.login_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'referer': 'https://my.vultr.com/',
            'origin': 'https://my.vultr.com',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'upgrade-insecure-requests': '1'
        }
        self.vultr_url = 'https://my.vultr.com/'
        self.captcha_url = 'https://my.vultr.com/_images/captcha.php?s={}'
        self.session.headers.update(self.headers)


'''移动端登录Vultr'''
class vultrMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in vultr in mobile mode'


'''扫码登录Vultr'''
class vultrScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in vultr in scanqr mode'


'''
Function:
    Vultr模拟登录
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
class vultr():
    def __init__(self, **kwargs):
        self.info = 'login in vultr'
        self.supported_modes = {
            'pc': vultrPC(**kwargs),
            'mobile': vultrMobile(**kwargs),
            'scanqr': vultrScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in vultr.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in vultr.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)