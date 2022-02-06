'''
Function:
    B站模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-02-06
'''
import rsa
import time
import base64
import urllib
import hashlib
import requests


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
        # 是否需要验证码
        is_need_captcha = False
        while True:
            # 需要验证码
            if is_need_captcha:
                captcha_img = self.session.get(self.captcha_url, headers=self.captcha_headers).content
                data = {'image': base64.b64encode(captcha_img).decode('utf-8')}
                captcha = self.session.post(self.crack_captcha_url, json=data).json()['message']
            # 获得key值
            appkey = 'bca7e84c2d947ac6'
            data = {
                'appkey': appkey,
                'sign': self.__calcSign('appkey={}'.format(appkey))
            }
            response = self.session.post(self.getkey_url, data=data)
            response_json = response.json()
            key_hash = response_json['data']['hash']
            pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(response_json['data']['key'].encode('utf-8'))
            # 模拟登录
            if is_need_captcha:
                data = "access_key=&actionKey=appkey&appkey={}&build=6040500&captcha={}&challenge=&channel=bili&cookies=&device=phone&mobi_app=android&password={}&permission=ALL&platform=android&seccode=&subid=1&ts={}&username={}&validate=" \
                        .format(appkey, captcha, urllib.parse.quote_plus(base64.b64encode(rsa.encrypt('{}{}'.format(key_hash, password).encode(), pub_key))), int(time.time()), urllib.parse.quote_plus(username))
            else:
                data = "access_key=&actionKey=appkey&appkey={}&build=6040500&captcha=&challenge=&channel=bili&cookies=&device=phone&mobi_app=android&password={}&permission=ALL&platform=android&seccode=&subid=1&ts={}&username={}&validate=" \
                        .format(appkey, urllib.parse.quote_plus(base64.b64encode(rsa.encrypt('{}{}'.format(key_hash, password).encode(), pub_key))), int(time.time()), urllib.parse.quote_plus(username))
            data = "{}&sign={}".format(data, self.__calcSign(data))
            response = self.session.post(self.login_url, data=data, headers=self.login_headers)
            response_json = response.json()
            # 不需要验证码, 登录成功
            if response_json['code'] == 0 and response_json['data']['status'] == 0:
                for cookie in response_json['data']['cookie_info']['cookies']:
                    self.session.cookies.set(cookie['name'], cookie['value'], domain='.bilibili')
                print('[INFO]: Account -> %s, login successfully' % username)
                infos_return = {'username': username}
                infos_return.update(response_json)
                return infos_return, self.session
            # 需要识别验证码
            elif response_json['code'] == -105:
                is_need_captcha = True
            # 账号密码错误
            elif response_json['code'] == -629:
                raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
            # 其他错误
            else:
                raise RuntimeError(response_json.get('data', {}).get('message'))
    '''计算sign值'''
    def __calcSign(self, param, salt="60698ba2f68e01ce44738920a0ffe768"):
        sign = hashlib.md5('{}{}'.format(param, salt).encode('utf-8'))
        return sign.hexdigest()
    '''初始化'''
    def __initialize(self):
        self.login_headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        self.captcha_headers = {
            'Host': 'passport.bilibili.com'
        }
        self.getkey_url = 'https://passport.bilibili.com/api/oauth2/getKey'
        self.login_url = 'https://passport.bilibili.com/api/v3/oauth2/login'
        self.captcha_url = 'https://passport.bilibili.com/captcha'
        # 破解网站来自: https://github.com/Hsury/Bilibili-Toolkit
        self.crack_captcha_url = 'https://bili.dev:2233/captcha'
        self.session.headers.update({'User-Agent': "Mozilla/5.0 BiliDroid/5.51.1 (bbcallen@gmail.com)"})


'''扫码登录B站'''
class bilibiliScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in bilibili in scanqr mode'


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
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
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