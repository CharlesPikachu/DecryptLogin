'''
Function:
    QQ音乐模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-11-01
'''
import os
import re
import time
import random
import warnings
import requests
from ..utils.misc import *
warnings.filterwarnings('ignore')


'''PC端登录QQ音乐'''
class qqmusicPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in qqmusic in pc mode'


'''移动端登录QQ音乐'''
class qqmusicMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in qqmusic in mobile mode'


'''扫码登录QQ音乐'''
class qqmusicScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in qqmusic in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得pt_login_sig
        params = {
            'appid': '716027609',
            'daid': '383',
            'style': '33',
            'login_text': '授权并登录',
            'hide_title_bar': '1',
            'hide_border': '1',
            'target': 'self',
            's_url': 'https://graph.qq.com/oauth2.0/login_jump',
            'pt_3rd_aid': '100497308',
            'pt_feedback_link': 'https://support.qq.com/products/77942?customInfo=.appid100497308',
        }
        response = self.session.get(self.xlogin_url, params=params)
        pt_login_sig = self.session.cookies.get('pt_login_sig')
        # 获取二维码
        params = {
            'appid': '716027609',
            'e': '2',
            'l': 'M',
            's': '3',
            'd': '72',
            'v': '4',
            't': str(random.random()),
            'daid': '383',
            'pt_3rd_aid': '100497308',
        }
        response = self.session.get(self.ptqrshow_url, params=params)
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        qrsig = self.session.cookies.get('qrsig')
        ptqrtoken = self.__decryptQrsig(qrsig)
        # 检测二维码状态
        while True:
            params = {
                'u1': 'https://graph.qq.com/oauth2.0/login_jump',
                'ptqrtoken': ptqrtoken,
                'ptredirect': '0',
                'h': '1',
                't': '1',
                'g': '1',
                'from_ui': '1',
                'ptlang': '2052',
                'action': '0-0-%s' % int(time.time() * 1000),
                'js_ver': '20102616',
                'js_type': '1',
                'login_sig': pt_login_sig,
                'pt_uistyle': '40',
                'aid': '716027609',
                'daid': '383',
                'pt_3rd_aid': '100497308',
                'has_onekey': '1',
            }
            response = self.session.get(self.ptqrlogin_url, params=params)
            if '登录成功' in response.text:
                break
            elif '二维码已经失效' in response.text:
                raise RuntimeError('Fail to login, qrcode has expired')
            time.sleep(0.5)
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 登录成功
        infos_return = {'data': response.text}
        qq_number = re.findall(r'&uin=(.+?)&service', response.text)[0]
        url_refresh = re.findall(r"'(https:.*?)'", response.text)[0]
        response = self.session.get(url_refresh, allow_redirects=False, verify=False)
        print('[INFO]: Account -> %s, login successfully' % qq_number)
        infos_return.update({'username': qq_number})
        return infos_return, self.session
    '''qrsig转ptqrtoken, hash33函数'''
    def __decryptQrsig(self, qrsig):
        e = 0
        for c in qrsig:
            e += (e << 5) + ord(c)
        return 2147483647 & e
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.ptqrshow_url = 'https://ssl.ptlogin2.qq.com/ptqrshow?'
        self.xlogin_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?'
        self.ptqrlogin_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?'
        self.session.headers.update(self.headers)


'''
Function:
    QQ音乐模拟登录
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
class qqmusic():
    def __init__(self, **kwargs):
        self.info = 'login in qqmusic'
        self.supported_modes = {
            'pc': qqmusicPC(**kwargs),
            'mobile': qqmusicMobile(**kwargs),
            'scanqr': qqmusicScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in qqmusic.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in qqmusic.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)