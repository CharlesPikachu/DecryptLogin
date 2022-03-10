'''
Function:
    去哪儿旅行模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-11-07
'''
import os
import re
import time
import requests
from ..utils.misc import *


'''PC端登录去哪儿旅行'''
class qunarPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in qunar in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化cookies
        response = self.session.get(self.home_url)
        # 获取验证码
        response = self.session.get(self.captcha_url % str(int(time.time() * 1000)))
        saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
        if crack_captcha_func is None:
            showImage(os.path.join(self.cur_path, 'captcha.jpg'))
            captcha = input('Input the captcha: ')
        else:
            captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
        removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
        # 设置cookies
        self.session.get(self.addICK_url)
        response = self.session.get(self.sessionId_url)
        session_id = re.findall(r'sessionId=(.*?)&', response.text)[0]
        self.session.get(self.fid_url % session_id)
        self.session.cookies.update({'QN271': session_id})
        # 模拟登录
        data = {
            'loginType': '0',
            'ret': 'https://www.qunar.com/',
            'username': username,
            'password': password,
            'remember': '1',
            'vcode': captcha
        }
        response = self.session.post(self.login_url, data=data)
        response_json = response.json()
        # 登录成功
        if response_json['ret'] and (response_json['errcode'] == 0):
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号或密码有误
        elif response_json['errcode'] in [21022]:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 验证码有误
        elif response_json['errcode'] in [11004]:
            raise RuntimeError('Account -> %s, fail to login, crack captcha error' % username)
        # 账号安全问题, 需要短信验证
        elif response_json['errcode'] in [21035]:
            response = self.session.get(self.captcha_url % str(int(time.time() * 1000)))
            saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
            if crack_captcha_func is None:
                showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                captcha = input('Input the captcha: ')
            else:
                captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
            removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
            self.session.get(self.addICK_url)
            response = self.session.get(self.sessionId_url)
            session_id = re.findall(r'sessionId=(.*?)&', response.text)[0]
            self.session.get(self.fid_url % session_id)
            self.session.cookies.update({'QN271': session_id})
            data = {
                'mobile': username,
                'vcode': captcha,
                'type': '3',
            }
            response = self.session.post(self.getLoginCode_url, data=data)
            if 'success' not in response.text:
                raise RuntimeError(response.json().get('errmsg', 'something error when get sms code'))
            code = input('This login is detected to be at risk, please enter the sms code your phone have accepted: ')
            data = {
                'loginType': '1',
                'ret': 'https://www.qunar.com/',
                'mobile': username,
                'randcode': code,
                'remember': '1',
            }
            response = self.session.post(self.login_url, data=data)
            response_json = response.json()
            if response_json['errcode'] == 0:
                print('[INFO]: Account -> %s, login successfully' % username)
                infos_return = {'username': username}
                infos_return.update(response_json)
                return infos_return, self.session
            else:
                raise RuntimeError(response_json.get('errmsg'))
        # 其他原因
        else:
            raise RuntimeError(response_json.get('errmsg'))
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }
        self.home_url = 'http://user.qunar.com/passport/login.jsp'
        self.captcha_url = 'https://user.qunar.com/captcha/api/image?k={en7mni(z&p=ucenter_login&c=ef7d278eca6d25aa6aec7272d57f0a9a&t=%s'
        self.addICK_url = 'https://user.qunar.com/passport/addICK.jsp?ssl'
        self.sessionId_url = 'https://rmcsdf.qunar.com/js/df.js?org_id=ucenter.login&js_type=0'
        self.fid_url = 'https://rmcsdf.qunar.com/api/device/challenge.json?sessionId=%s&domain=qunar.com&orgId=ucenter.login'
        self.login_url = 'https://user.qunar.com/passport/loginx.jsp'
        self.getLoginCode_url = 'http://user.qunar.com/passport/getLoginCode.jsp'
        self.session.headers.update(self.headers)


'''移动端登录去哪儿旅行'''
class qunarMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in qunar in mobile mode'


'''扫码登录去哪儿旅行'''
class qunarScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in qunar in scanqr mode'


'''
Function:
    去哪儿旅行模拟登录
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
class qunar():
    def __init__(self, **kwargs):
        self.info = 'login in qunar'
        self.supported_modes = {
            'pc': qunarPC(**kwargs),
            'mobile': qunarMobile(**kwargs),
            'scanqr': qunarScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in qunar.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in qunar.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)