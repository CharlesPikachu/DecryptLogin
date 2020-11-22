'''
Function:
    QQ群模拟登录
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
import warnings
import requests
from ..utils.misc import *
warnings.filterwarnings('ignore')


'''PC端登录QQ群'''
class QQQunPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in QQQun in pc mode'


'''移动端登录QQ群'''
class QQQunMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in QQQun in mobile mode'


'''扫码登录QQ群'''
class QQQunScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in QQQun in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 保存cookies的字典
        all_cookies = {}
        # 获取pt_login_sig
        params = {
            'appid': '549000912',
            's_url': 'http://qun.qq.com/member.html'
        }
        response = self.session.get(self.login_url, headers=self.headers, verify=False, params=params)
        all_cookies.update(requests.utils.dict_from_cookiejar(response.cookies))
        pt_login_sig = all_cookies['pt_login_sig']
        # 获得ptqrtoken
        params = {
            'appid': '549000912',
            'e': '2',
            'l': 'M',
            's': '3',
            'd': '72',
            'v': '4',
            't': str(random.random()),
            'pt_3rd_aid': '0'
        }
        response = self.session.get(self.qrshow_url, headers=self.headers, verify=False, params=params)
        all_cookies.update(requests.utils.dict_from_cookiejar(response.cookies))
        ptqrtoken = self.__decryptQrsig(all_cookies['qrsig'])
        # 保存二维码图片
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        self.session.cookies.update(all_cookies)
        # 检测二维码状态
        while True:
            params = {
                'u1': 'http://qun.qq.com/member.html',
                'ptqrtoken': ptqrtoken,
                'ptredirect': '1',
                'h': '1',
                't': '1',
                'g': '1',
                'from_ui': '1',
                'ptlang': '2052',
                'action': '0-0-' + str(int(time.time())),
                'js_ver': '19112817',
                'js_type': '1',
                'login_sig': pt_login_sig,
                'pt_uistyle': '40',
                'aid': '549000912',
                'has_onekey': '1'
            }
            response = self.session.get(self.qrlogin_url, headers=self.headers, verify=False, params=params)
            if '登录成功' in response.text:
                break
            elif '二维码已经失效' in response.text:
                raise RuntimeError('Fail to login, qrcode has expired')
            time.sleep(2)
        # 登录成功
        all_cookies.update(requests.utils.dict_from_cookiejar(response.cookies))
        qq_number = re.findall(r'&uin=(.+?)&service', response.text)[0]
        url_refresh = response.text[response.text.find('http'): response.text.find('pt_3rd_aid=0')] + 'pt_3rd_aid=0'
        self.session.cookies.update(all_cookies)
        response = self.session.get(url_refresh, allow_redirects=False, verify=False)
        all_cookies.update(requests.utils.dict_from_cookiejar(response.cookies))
        self.session.cookies.update(all_cookies)
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        print('[INFO]: Account -> %s, login successfully' % qq_number)
        infos_return = {'username': qq_number}
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.login_url = 'http://ui.ptlogin2.qq.com/cgi-bin/login?'
        self.qrshow_url = 'https://ssl.ptlogin2.qq.com/ptqrshow?'
        self.qrlogin_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?'


'''
Function:
    QQ群模拟登录
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
class QQQun():
    def __init__(self, **kwargs):
        self.info = 'login in QQQun'
        self.supported_modes = {
            'pc': QQQunPC(**kwargs),
            'mobile': QQQunMobile(**kwargs),
            'scanqr': QQQunScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in QQQun.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in QQQun.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)