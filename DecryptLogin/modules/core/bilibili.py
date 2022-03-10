'''
Function:
    B站模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-09
'''
import os
import rsa
import time
import random
import qrcode
import base64
import urllib
import hashlib
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from ..utils import showImage, removeImage


'''PC端登录B站'''
class bilibiliPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in bilibili in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 手动过验证码
        response = self.session.get(self.captcha_url)
        if response.status_code != 200: raise RuntimeError(response.text)
        response_json = response.json()
        if response_json['code'] != 0: raise RuntimeError(response.json())
        gt = response_json['data']['result']['gt']
        challenge = response_json['data']['result']['challenge']
        key = response_json['data']['result']['key']
        print(f'[INFO]: gt is {gt} and challenge is {challenge}')
        print('[INFO]: Please visit https://kuresaru.github.io/geetest-validator/ to obtain validate and seccode')
        validate = input('validate: ')
        seccode = input('seccode: ')
        # 模拟登录
        response = self.session.get(self.getkey_url)
        response_json = response.json()
        password_encrypt = self.encrypt(response_json['key'].encode('utf-8'), (response_json['hash'] + password).encode('utf-8'))
        data = f'captchaType=6&username={username}&password={password_encrypt.decode("utf-8")}&keep=true&key={key}&challenge={challenge}&validate={validate}&seccode={seccode}'
        response = self.session.post(self.login_url, headers=self.login_headers, data=data)
        response_json = response.json()
        # 判断是否存在安全风险
        if 'passport.bilibili.com/account/mobile/security/managephone/phone/verify' in response.text:
            response_json = bilibiliMobile().loginbysms(username)
        # 登录成功
        if response_json['code'] == 0:
            response = self.session.get(response_json['data']['redirectUrl'])
            response_json['response_text'] = response.text
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号密码错误
        elif response_json['code'] == -629:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise RuntimeError(response_json.get('data', {}))
    '''加密'''
    def encrypt(self, public_key, data):
        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
        return base64.urlsafe_b64encode(rsa.encrypt(data, pub_key))
    '''初始化'''
    def __initialize(self):
        self.login_headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        self.getkey_url = 'https://passport.bilibili.com/login?act=getkey'
        self.login_url = 'https://passport.bilibili.com/web/login/v2'
        self.captcha_url = 'https://passport.bilibili.com/web/captcha/combine?plat=6'


'''移动端登录B站'''
class bilibiliMobile():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in bilibili in mobile mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 加密
        response = self.session.get(self.key_url)
        hash_value, public_key = response.json()['data']['hash'], response.json()['data']['key']
        public_key = RSA.importKey(public_key)
        password = hash_value + password
        cipher = PKCS1_v1_5.new(public_key)
        password = str(base64.b64encode(cipher.encrypt(password.encode('utf-8'))), 'utf-8')
        # 模拟登录
        data = {
            'captcha': '',
            'challenge': '',
            'cookies': '',
            'password': password,
            'permission': 'ALL',
            'seccode': '',
            'subid': '1',
            'username': username,
            'validate': '',
            'access_key': '',
            'actionKey': 'appkey',
            'appkey': '783bbb7264451d82',
            'build': '6550400',
            'channel': 'bili',
            'device': 'phone',
            'mobi_app': 'android',
            'platform': 'android',
            'ts': str(int(time.time())),
        }
        keys = sorted(data.keys())
        data_sorted = {}
        for key in keys: data_sorted[key] = data[key]
        data = data_sorted
        sign = self.__calcSign(data)
        data.update({'sign': sign})
        response = self.session.post(self.login_url, data=data, headers=self.headers)
        response_json = response.json()
        # 判断是否存在安全风险
        if 'passport.bilibili.com/account/mobile/security/managephone/phone/verify' in response.text:
            response_json = self.loginbysms(username)
        # 登录成功
        if response_json['code'] == 0 and response_json['data']['status'] == 0:
            for cookie in response_json['data']['cookie_info']['cookies']:
                self.session.cookies.set(cookie['name'], cookie['value'], domain='.bilibili')
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号密码错误
        elif response_json['code'] == -629:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise RuntimeError(response_json.get('data', {}))
    '''计算sign值'''
    def __calcSign(self, param, salt="2653583c8873dea268ab9386918b1d65"):
        param = urllib.parse.urlencode(param)
        sign = hashlib.md5('{}{}'.format(param, salt).encode('utf-8'))
        return sign.hexdigest()
    '''伪造buvid'''
    def __fakebuvid(self):
        mac_list = []
        for i in range(1, 7):
            rand_str = ''.join(random.sample('0123456789abcdef', 2))
            mac_list.append(rand_str)
        rand_mac = ':'.join(mac_list)
        md5 = hashlib.md5()
        md5.update(rand_mac.encode())
        md5_mac_str = md5.hexdigest()
        md5_mac = list(md5_mac_str)
        fake_mac = ('XY' + md5_mac[2] + md5_mac[12] + md5_mac[22] + md5_mac_str).upper()
        return fake_mac
    '''通过SMS登录'''
    def loginbysms(self, username):
        default = {
            'access_key': '',
            'actionKey': 'appkey',
            'appkey': '783bbb7264451d82',
            'build': '6590300',
            'channel': 'bili',
            'device': 'phone',
            'mobi_app': 'android',
            'platform': 'android',
            'ts': str(int(time.time())),
        }
        # 发送验证码
        data = {
            'cid': '86',
            'tel': username,
            'statistics': '{"appId":1,"platform":3,"version":"6.32.0","abtest":""}'
        }
        data, data_sorted = {**data, **default}, {}
        for key in sorted(data.keys()):
            data_sorted.update({key: data[key]})
        data = data_sorted
        sign = self.__calcSign(data)
        data.update({'sign': sign})
        response = self.session.post(self.send_url, headers=self.headers, data=data)
        # 验证登录
        captcha_key = response.json()['data']['captcha_key']
        code = input(f'Due to the risk of this login, input the sms code sent to {username}: ')
        data_sms = {
            'captcha_key': captcha_key,
            'cid': data['cid'],
            'tel': data['tel'],
            'statistics': data['statistics'],
            'code': code,
        }
        data_sms, data_sms_sorted = {**data_sms, **default}, {}
        for key in sorted(data_sms.keys()):
            data_sms_sorted.update({key: data_sms[key]})
        data_sms = data_sms_sorted
        sign = self.__calcSign(data_sms)
        data_sms.update({'sign': sign})
        response = self.session.post(self.sms_url, headers=self.headers, data=data_sms)
        # 返回
        return response.json()
    '''初始化'''
    def __initialize(self):
        self.login_url = 'https://passport.bilibili.com/x/passport-login/oauth2/login'
        self.key_url = 'https://passport.bilibili.com/x/passport-login/web/key'
        self.send_url = 'https://passport.bilibili.com//x/passport-login/sms/send'
        self.sms_url = 'https://passport.bilibili.com/x/passport-login/login/sms'
        self.headers = {
            'env': 'prod',
            'APP-KEY': 'android',
            'Buvid': self.__fakebuvid(),
            'Accept': '*/*',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 BiliDroid/6.55.0 (bbcalllen@gmail.com) os/android model/MuMu mobi_app/android build/6550400 channel/bili innerVer/6550400 osVer/7.1.2 network/2',
        }


'''扫码登录B站'''
class bilibiliScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in bilibili in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得登录信息
        response = self.session.get(self.getLogin_url)
        response_json = response.json()
        scan_url, oauthKey = response_json['data']['url'], response_json['data']['oauthKey']
        # 制作二维码
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
        qr.add_data(scan_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img.save(os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 扫码
        headers = self.headers.copy()
        headers['Host'] = 'passport.bilibili.com'
        headers['Referer'] = 'https://passport.bilibili.com/login'
        while True:
            response = self.session.post(self.getLoginInfo_url, data={'oauthKey': oauthKey}, headers=headers)
            if response.json()['status']: break
            elif response.json()['data'] in [-4, -5]: time.sleep(0.5)
            else: raise RuntimeError(response.json())
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        response = self.session.get(response.json()['data']['url'])
        response = self.session.get(self.nav_url)
        response_json = response.json()
        username = response_json['data']['uname']
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
        }
        self.getLogin_url = 'https://passport.bilibili.com/qrcode/getLoginUrl'
        self.getLoginInfo_url = 'https://passport.bilibili.com/qrcode/getLoginInfo'
        self.nav_url = 'https://api.bilibili.com/x/web-interface/nav'
        self.session.headers.update(self.headers)


'''
Function:
    B站模拟登录
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
class bilibili():
    def __init__(self, **kwargs):
        self.info = 'login in bilibili'
        self.supported_modes = {
            'pc': bilibiliPC(**kwargs),
            'mobile': bilibiliMobile(**kwargs),
            'scanqr': bilibiliScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in bilibili.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in bilibili.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)