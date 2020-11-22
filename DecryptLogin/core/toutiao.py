'''
Function:
    今日头条模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-30
'''
import os
import time
import string
import base64
import random
import requests
from ..utils.misc import *


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
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 先访问头条主页
        self.session.get(url=self.home_url, headers=self.headers)
        # 无验证码登录尝试
        params = {
            'account_sdk_version': '341',
            'device_id': str(random.randrange(10**10, 10**11)),
            'ac': 'wifi',
            'channel': 'baidu',
            'aid': '13',
            'app_name': 'news_article',
            'version_code': '700',
            'version_name': '7.0.0',
            'device_platform': 'android',
            'abflag': '3',
            'ssmix': 'a',
            'os_api': '22',
            'os_version': '5.1.1',
            'manifest_version_code': '700',
            'update_version_code': '70011',
            '_rticket': str(int(time.time() * 1000)),
            'rom_version': '22',
            'plugin': '26958',
            'ts': str(int(time.time())),
            'tma_jssdk_version': '1.5.4.5'
        }
        data = {
            'mix_mode': '1',
            'password': self.__encrypt(password),
            'mobile': self.__encrypt(username),
            'ac': 'wifi',
            'channel': 'baidu',
            'aid': '13',
            'app_name': 'news_article',
            'version_code': '700',
            'version_name': '7.0.0',
            'device_platform': 'android',
            'abflag': '3',
            'ssmix': 'a',
            'os_api': '22',
            'os_version': '5.1.1',
            'manifest_version_code': '700',
            'update_version_code': '70011',
            '_rticket': str(int(time.time() * 1000)),
            'rom_version': '22',
            'plugin': '26958',
            'ts': str(int(time.time()))
        }
        response = self.session.post(url=self.login_url, data=data, params=params, headers=self.headers)
        response_json = response.json()
        # 登录失败
        if response_json['message'] == 'error':
            # --需要输入验证码
            if response_json['data']['error_code'] in [1101, 1102] and response_json['data']['captcha']:
                image = base64.b64decode(response_json['data']['captcha'])
                saveImage(image, os.path.join(self.cur_path, 'captcha.jpg'))
                if crack_captcha_func is None:
                    showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                    captcha = input('Input the captcha: ')
                else:
                    captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
                data['captcha'] = captcha
                response = self.session.post(url=self.login_url, data=data, headers=self.headers)
                response_json = response.json()
                if response_json['message'] == 'error':
                    raise RuntimeError(response_json['data']['description'])
            # --账号密码错误
            elif response_json['data']['error_code'] in [1009, 1003]:
                raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
            # --为保证帐号安全, 请使用手机验证码登录
            elif response_json['data']['error_code'] in [1039]:
                # ----发送手机验证码
                params = {
                    'account_sdk_version': '341',
                    'device_id': str(random.randrange(10**10, 10**11)),
                    'ac': 'wifi',
                    'channel': 'baidu',
                    'aid': '13',
                    'app_name': 'news_article',
                    'version_code': '700',
                    'version_name': '7.0.0',
                    'device_platform': 'android',
                    'abflag': '3',
                    'ssmix': 'a',
                    'os_api': '22',
                    'os_version': '5.1.1',
                    'manifest_version_code': '700',
                    'update_version_code': '70011',
                    '_rticket': str(int(time.time() * 1000)),
                    'rom_version': '22',
                    'plugin': '26958',
                    'ts': str(int(time.time())),
                    'tma_jssdk_version': '1.5.4.5'
                }
                data = {
                    'mix_mode': '1',
                    'check_register': '1',
                    'type': '3731',
                    'mobile': self.__encrypt(username),
                    'unbind_exist': '35',
                    'ac': 'wifi',
                    'channel': 'baidu',
                    'aid': '13',
                    'app_name': 'news_article',
                    'version_code': '700',
                    'version_name': '7.0.0',
                    'device_platform': 'android',
                    'abflag': '3',
                    'ssmix': 'a',
                    'os_api': '22',
                    'os_version': '5.1.1',
                    'manifest_version_code': '700',
                    'update_version_code': '70011',
                    '_rticket': str(int(time.time() * 1000)),
                    'rom_version': '22',
                    'plugin': '26958',
                    'ts': str(int(time.time()))
                }
                response = self.session.post(url=self.send_code_url, data=data, params=params, headers=self.headers)
                # ----提交手机验证码
                code = input('This login is detected to be at risk, please enter the sms code you have accepted: ')
                params = {
                    'account_sdk_version': '341',
                    'device_id': str(random.randrange(10**10, 10**11)),
                    'ac': 'wifi',
                    'channel': 'baidu',
                    'aid': '13',
                    'app_name': 'news_article',
                    'version_code': '700',
                    'version_name': '7.0.0',
                    'device_platform': 'android',
                    'abflag': '3',
                    'ssmix': 'a',
                    'os_api': '22',
                    'os_version': '5.1.1',
                    'manifest_version_code': '700',
                    'update_version_code': '70011',
                    '_rticket': str(int(time.time() * 1000)),
                    'rom_version': '22',
                    'plugin': '26958',
                    'ts': str(int(time.time())),
                    'tma_jssdk_version': '1.5.4.5'
                }
                data = {
                    'mix_mode': '1',
                    'mobile': self.__encrypt(username),
                    'code': self.__encrypt(code),
                    'ac': 'wifi',
                    'channel': 'baidu',
                    'aid': '13',
                    'app_name': 'news_article',
                    'version_code': '700',
                    'version_name': '7.0.0',
                    'device_platform': 'android',
                    'abflag': '3',
                    'ssmix': 'a',
                    'os_api': '22',
                    'os_version': '5.1.1',
                    'manifest_version_code': '700',
                    'update_version_code': '70011',
                    '_rticket': str(int(time.time() * 1000)),
                    'rom_version': '22',
                    'plugin': '26958',
                    'ts': str(int(time.time()))
                }
                response = self.session.post(url=self.sms_login_url, data=data, params=params, headers=self.headers)
                response_json = response.json()
                if response_json['message'] == 'error':
                    raise RuntimeError(response_json['data']['description'])
            # --其他问题
            else:
                raise RuntimeError(response_json['data']['description'])
        # 登录成功
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''加密'''
    def __encrypt(self, params):
        if not params:
            return ''
        tmp = []
        for item in params:
            t = ord(item)
            if t >= 0 and t <= 127:
                tmp.append(t)
            if t >= 128 and t <= 2047:
                tmp.append(192 | 31 & t >> 6)
                tmp.append(128 | 63 & t)
            if (t >= 2048 and t <= 55295) or (t >= 57344 and t <= 65535):
                tmp.append(224 | 15 & t >> 12)
                tmp.append(128 | 63 & t >> 6)
                tmp.append(128 | 63 & t)
        for i in range(len(tmp)):
            tmp[i] &= 255
        result = []
        for item in tmp:
            result.append(hex(5 ^ item))
        return ''.join([x.replace('0x', '') for x in result])
    '''初始化'''
    def __initialize(self):
        rands = string.ascii_letters + string.digits
        device_type = [random.choice(rands) for _ in range(random.randrange(1, 9))]
        device_type = random.choice(string.ascii_uppercase) + ''.join(device_type)
        rands = string.ascii_letters + string.digits
        builder = [random.choice(rands) for _ in range(random.randrange(1, 9))]
        builder = ''.join(builder)
        version = random.choice(string.digits)
        self.headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; %s Build/%s) NewsArticle/7.0.0 okhttp/3.10.0.%s' % (device_type, builder, version)
        }
        self.home_url = 'https://m.toutiao.com/'
        self.login_url = 'https://is-hl.snssdk.com/passport/mobile/login/'
        self.send_code_url = 'https://is-hl.snssdk.com/passport/mobile/send_code/'
        self.sms_login_url = 'https://is-hl.snssdk.com/passport/mobile/sms_login/'


'''扫码登录今日头条'''
class toutiaoScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in toutiao in scanqr mode'


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
    def login(self, username, password, mode='mobile', crack_captcha_func=None, **kwargs):
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