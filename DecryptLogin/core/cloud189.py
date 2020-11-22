'''
Function:
    天翼云盘模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-11-01
'''
import os
import re
import rsa
import base64
import requests
from ..utils.misc import *


'''PC端登录天翼云盘'''
class cloud189PC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in cloud189 in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化, 获取必要的登录参数
        params = {
            'pageId': '1',
            'redirectURL': '/main.action',
        }
        response = self.session.get(self.udb_login_url, params=params)
        captcha_token = re.search(r'captchaToken\W*value=\W*(\w*)', response.text).group(1)
        return_url = re.search(r'returnUrl =\W*([^\'"]*)', response.text).group(1)
        param_id = re.search(r'paramId =\W*(\w*)', response.text).group(1)
        lt = re.search(r'lt =\W+(\w*)', response.text).group(1)
        self.session.headers.update({'lt': lt})
        # 判断是否需要验证码
        data = {
            'accountType': '01',
            'userName': self.__encrypt(username),
            'appKey': 'cloud'
        }
        response = self.session.post(self.needcaptcha_url, data=data)
        captcha = ''
        if response.text != '0':
            response = self.session.get(self.picCaptcha_url, params={'token':captcha_token})
            saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
            if crack_captcha_func is None:
                showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                captcha = input('Input the captcha: ')
            else:
                captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
            removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
        # 模拟登录
        data = {
            'appKey': 'cloud',
            'accountType': '01',
            'userName': self.__encrypt(username),
            'password': self.__encrypt(password),
            'validateCode': captcha,
            'captchaToken': captcha_token,
            'returnUrl': return_url,
            'mailSuffix': '@189.cn',
            'paramId': param_id
        }
        response = self.session.post(self.loginSubmit_url, data=data)
        response_json = response.json()
        # 登录成功
        if response_json['msg'] == u'登录成功' and response_json['result'] == 0:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号或密码错误
        elif response_json['result'] in [-51002, -17]:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise RuntimeError(response_json.get('msg'))
    '''天翼云盘加密算法'''
    def __encrypt(self, data):
        def int2char(index):
            return list('0123456789abcdefghijklmnopqrstuvwxyz')[index]
        def b64tohex(a):
            b64map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
            d, e, c = '', 0, 0
            for i in range(len(a)):
                if list(a)[i] != '=':
                    v = b64map.index(list(a)[i])
                    if 0 == e:
                        e = 1
                        d += int2char(v >> 2)
                        c = 3 & v
                    elif 1 == e:
                        e = 2
                        d += int2char(c << 2 | v >> 4)
                        c = 15 & v
                    elif 2 == e:
                        e = 3
                        d += int2char(c)
                        d += int2char(v >> 2)
                        c = 3 & v
                    else:
                        e = 0
                        d += int2char(c << 2 | v >> 4)
                        d += int2char(15 & v)
            if e == 1: d += int2char(c << 2)
            return d
        rsa_key = '-----BEGIN PUBLIC KEY-----\n' \
            'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDY7mpaUysvgQkbp0iIn2ezoUyh\n' \
            'i1zPFn0HCXloLFWT7uoNkqtrphpQ/63LEcPz1VYzmDuDIf3iGxQKzeoHTiVMSmW6\n' \
            'FlhDeqVOG094hFJvZeK4OzA6HVwzwnEW5vIZ7d+u61RV1bsFxmB68+8JXs3ycGcE\n' \
            '4anY+YzZJcyOcEGKVQIDAQAB\n' \
            '-----END PUBLIC KEY-----'
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode('utf-8'))
        data_encrypt = b64tohex((base64.b64encode(rsa.encrypt(data.encode('utf-8'), pubkey))).decode('utf-8'))
        return '{RSA}' + data_encrypt
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Referer': 'https://open.e.189.cn/',
        }
        self.udb_login_url = 'https://cloud.189.cn/udb/udb_login.jsp'
        self.needcaptcha_url = 'https://open.e.189.cn/api/logbox/oauth2/needcaptcha.do'
        self.picCaptcha_url = 'https://open.e.189.cn/api/logbox/oauth2/picCaptcha.do'
        self.loginSubmit_url = 'https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do'
        self.session.headers.update(self.headers)


'''移动端登录天翼云盘'''
class cloud189Mobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in cloud189 in mobile mode'


'''扫码登录天翼云盘'''
class cloud189Scanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in cloud189 in scanqr mode'


'''
Function:
    天翼云盘模拟登录
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
class cloud189():
    def __init__(self, **kwargs):
        self.info = 'login in cloud189'
        self.supported_modes = {
            'pc': cloud189PC(**kwargs),
            'mobile': cloud189Mobile(**kwargs),
            'scanqr': cloud189Scanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in cloud189.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in cloud189.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)