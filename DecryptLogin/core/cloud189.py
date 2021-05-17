'''
Function:
    天翼云盘模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2021-05-17
'''
import os
import re
import rsa
import uuid
import base64
import hashlib
import requests
from urllib import parse
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
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in cloud189 in mobile mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 检查是否需要验证码
        assert not self.__needcaptcha(username, password), 'Unsupport the situation that needs captcha'
        # 设备信息
        device_info = {
            'imei': '',
            'imsi': '',
            'deviceId': self.__md5(username + password),
            'terminalInfo': 'Mi MIX3',
            'osInfo': 'Android:10',
            'mobileBrand': 'Xiaomi',
            'mobileModel': 'Mi MIX3',
        }
        device_info = str(device_info).replace("'", '"')
        # 模拟登录
        data = {
            'appKey': 'cloud',
            'deviceInfo': self.__encrypthex(device_info),
            'apptype': 'wap',
            'loginType': '1',
            'dynamicCheck': 'false',
            'userName': '{RSA}' + self.__rsaencrypthex(username),
            'password': '{RSA}' + self.__rsaencrypthex(password),
            'validateCode': '',
            'captchaToken': '',
            'jointWay': '1|2',
            'jointVersion': 'v3.8.1',
            'operator': '',
            'nwc': 'WIFI',
            'nws': '2',
            'guid': self.__md5(password),
            'reqId': 'undefined',
            'headerDeviceId': self.__md5(password),
        }
        headers = self.headers.copy()
        headers.update({
            'X-Requested-With': 'com.cn21.ecloud',
            'X-Request-Id': str(uuid.uuid4),
            'Host': parse.urlparse(self.login_url).hostname
        })
        response = self.session.post(self.login_url, data=data, headers=headers)
        response_json = response.json()
        # 登录失败
        if str(response_json['result']) != '0':
            raise RuntimeError(response_json['msg'])
        # 登录成功
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username}
        response_json['returnParas_decrypt'] = parse.parse_qs(self.__decrypthex(parse.parse_qs(response_json['returnParas']).get('paras')[0]))
        infos_return.update(response_json)
        return infos_return, self.session
    '''检查是否需要验证码'''
    def __needcaptcha(self, username, password):
        data = {
            'appKey': 'cloud',
            'userName': '{RSA}' + self.__rsaencrypthex(username),
            'guid': self.__md5(password),
            'reqId': 'undefined',
            'headerDeviceId': self.__md5(password),
        }
        headers = {
            'X-Requested-With': 'com.cn21.ecloud',
            'X-Request-Id': str(uuid.uuid4),
            'Host': parse.urlparse(self.needcaptcha_url).hostname
        }
        response = self.session.post(self.needcaptcha_url, data=data, headers=headers)
        if response.text != '0': return True
        return False
    '''md5'''
    def __md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    '''encrypt data with the public key of base64 to hex string'''
    def __rsaencrypthex(self, data, public_key=None):
        if public_key is None: 
            rsa_public_key = rsa.PublicKey(152334346597938436293356441115719435124636105143326532780542577723094703991678344742000021867588140450685721745211231553599381639990706123205672974928645595682727909568532858444056192955490635499533969753560238390855204373585601526650632417250726199698579300301057558260951102971295524642685968805111112239701, 65537)
        else:
            rsa_public_key = rsa.PublicKey.load_pkcs1_openssl_pem(f'-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----'.encode('utf-8'))
        return rsa.encrypt(data.encode('utf-8'), rsa_public_key).hex()
    '''encrypt str data to hex string'''
    def __encrypthex(self, data):
        try:
            import xxtea
        except:
            raise ImportError('Try to run "pip install xxtea-py" for using xxtea')
        return xxtea.encrypt(data, bytes.fromhex('67377150343554566b51354736694e6262686155356e586c41656c4763416373')).hex()
    '''decrypt hex string data to str'''
    def __decrypthex(self, data):
        try:
            import xxtea
        except:
            raise ImportError('Try to run "pip install xxtea-py" for using xxtea')
        return xxtea.decrypt_utf8(bytes.fromhex(data), bytes.fromhex('67377150343554566b51354736694e6262686155356e586c41656c4763416373'))
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mi MIX3 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.66 Mobile Safari/537.36 clientCtaSdkVersion/v3.8.1 deviceSystemVersion/10 deviceSystemType/Android clientPackageName/com.cn21.ecloud clientPackageNameSign/1c71af12beaa24e4d4c9189f3c9ad576'
        }
        self.needcaptcha_url = 'https://open.e.189.cn/api/logbox/oauth2/needcaptcha.do'
        self.login_url = 'https://open.e.189.cn/api/logbox/oauth2/oAuth2SdkLoginByPassword.do'
        self.session.headers.update(self.headers)


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