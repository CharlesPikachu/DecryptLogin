'''
Function:
    微信公众号模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-30
'''
import os
import time
import random
import hashlib
import requests
import warnings
from ..utils.misc import *
warnings.filterwarnings('ignore')


'''PC端登录微信公众号'''
class mpweixinPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in mpweixin in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 模拟登录
        data = {
            'username': username,
            'pwd': hashlib.md5(password.encode('utf-8')).hexdigest(),
            'imgcode': '',
            'f': 'json'
        }
        response = self.session.post(self.startlogin_url, data=data, verify=False)
        response_json = response.json()
        # 请求有误
        if response_json['base_resp']['ret'] != 0:
            # --账户或密码错误
            if response_json['base_resp']['ret'] in [200023]:
                raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
            # --其他
            else:
                raise RuntimeError(response_json['base_resp']['err_msg'])
        # 保障账号安全, 还需要微信扫码
        response = self.session.get(self.getqrcode_url, verify=False)
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检测二维码状态
        while True:
            response = self.session.get(self.ask_url, verify=False)
            response_json = response.json()
            # --扫码成功
            if response_json['status'] == 1:
                break
            # --等待扫码/正在扫码
            elif response_json['status'] in [0, 4]:
                pass
            # --其他原因
            else:
                raise RuntimeError(response_json['base_resp']['err_msg'])
            time.sleep(1)
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 模拟登录
        data = {
            'f': 'json',
            'ajax': '1',
            'random': str(random.random())
        }
        response = self.session.post(self.login_url, data=data, verify=False)
        response_json = response.json()
        # 登录成功
        if response_json['base_resp']['ret'] == 0:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 其他
        else:
            raise RuntimeError(response_json['base_resp']['err_msg'])
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Referer': 'https://mp.weixin.qq.com/'
        }
        self.startlogin_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin'
        self.getqrcode_url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300'
        self.ask_url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1'
        self.login_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login'
        self.session.headers.update(self.headers)


'''移动端登录微信公众号'''
class mpweixinMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in mpweixin in mobile mode'


'''扫码登录微信公众号'''
class mpweixinScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in mpweixin in scanqr mode'


'''
Function:
    微信公众号模拟登录
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
class mpweixin():
    def __init__(self, **kwargs):
        self.info = 'login in mpweixin'
        self.supported_modes = {
            'pc': mpweixinPC(**kwargs),
            'mobile': mpweixinMobile(**kwargs),
            'scanqr': mpweixinScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in mpweixin.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in mpweixin.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)