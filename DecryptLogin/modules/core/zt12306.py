'''
Function:
    12306模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import os
import time
import requests
from ..utils.misc import *


'''PC端登录12306'''
class zt12306PC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zt12306 in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 下载验证码
        self.__downloadCaptcha()
        time.sleep(0.1)
        # 验证码验证
        response = self.__verifyCaptcha(crack_captcha_func)
        if not response:
            raise RuntimeError('Account -> %s, fail to login, crack captcha error' % username)
        # 模拟登录
        data = {
            'username': username,
            'password': password,
            'appid': 'otn'
        }
        response = self.session.post(self.login_url, headers=self.headers, data=data)
        # 登录成功
        if response.status_code == 200:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            return infos_return, self.session
        # 登录失败
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
    '''下载验证码'''
    def __downloadCaptcha(self):
        response = self.session.get(self.captcha_url, headers=self.headers)
        saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
        return True
    '''验证码验证'''
    def __verifyCaptcha(self, crack_captcha_func):
        img_path = os.path.join(self.cur_path, 'captcha.jpg')
        if crack_captcha_func is None:
            showImage(img_path)
            user_enter = input('Enter the positions of captcha, use <,> to separate, such as <2,3>\n(From left to right, top to bottom -> 1,2,3,4,5,6,7,8): ')
        else:
            user_enter = crack_captcha_func(img_path)
        digital_list = []
        for each in user_enter.split(','):
            each = each.strip()
            try:
                digital_list.append(self.positions[int(each)-1])
            except:
                raise RuntimeError('captcha format error...')
        data = {
            'answer': ','.join(digital_list),
            'login_site': 'E',
            'rand': 'sjrand'
        }
        response = self.session.post(url=self.captcha_check_url, headers=self.headers, data=data)
        removeImage(img_path)
        if response.json()['result_code'] == '4': return True
        return False
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.positions = ['36,46', '109,44', '181,47', '254,44', '33,112', '105,116', '186,116', '253,115']
        self.captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5579044251920726'
        self.captcha_check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.login_url = 'https://kyfw.12306.cn/passport/web/login'


'''移动端登录12306'''
class zt12306Mobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zt12306 in mobile mode'


'''扫码登录12306'''
class zt12306Scanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zt12306 in scanqr mode'


'''
Function:
    12306模拟登录
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
class zt12306():
    def __init__(self, **kwargs):
        self.info = 'login in zt12306'
        self.supported_modes = {
            'pc': zt12306PC(**kwargs),
            'mobile': zt12306Mobile(**kwargs),
            'scanqr': zt12306Scanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in zt12306.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in zt12306.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)