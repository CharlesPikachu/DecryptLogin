'''
Function:
    小米商城模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
import re
import time
import json
import random
import hashlib
import requests


'''PC端登录小米商城'''
class mieshopPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in mieshop in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化cookies
        device_id = ''.join(map(lambda i: chr(i), [random.randint(97, 122) for _ in range(6)]))
        self.session.cookies.set("sdkVersion", "accountsdk-18.8.15", domain="mi.com")
        self.session.cookies.set("sdkVersion", "accountsdk-18.8.15", domain="xiaomi.com")
        self.session.cookies.set("deviceId", device_id, domain="mi.com")
        self.session.cookies.set("deviceId", device_id, domain="xiaomi.com")
        # 获得sign等值
        response = self.session.get(self.sign_url, verify=False, params={'sid': 'mi_eshop', '_json': 'true'})
        sign = re.findall(r'"_sign":"(.*?)",', response.text)[0]
        qs = re.findall(r'"qs":"(.*?)",', response.text)[0]
        callback = re.findall(r'"callback":"(.*?)"', response.text)[0]
        # 模拟登录
        data = {
            '_json': 'true',
            'callback': callback,
            'sid': 'mi_eshop',
            'qs': qs,
            '_sign': sign,
            'serviceParam': '{"checkSafePhone":false,"checkSafeAddress":false}',
            'user': username,
            'hash': hashlib.md5(password.encode(encoding='utf-8')).hexdigest().upper(),
            'cc': '',
            'log': '{"title":"dataCenterZone","message":"China"}{"title":"locale","message":"zh_CN"}{"title":"env","message":"release"}{"title":"browser","message":{"name":"Chrome","version":78}}{"title":"search","message":"?callback=http%3A%2F%2Forder.mi.com%2Flogin%2Fcallback%3Ffollowup%3Dhttps%253A%252F%252Fwww.mi.com%252F%26sign%3DNzY3MDk1YzczNmUwMGM4ODAxOWE0NjRiNTU5ZGQyMzFhYjFmOGU0Nw%2C%2C&sid=mi_eshop&_bannerBiz=mistore&_qrsize=180"}{"title":"outerlinkDone","message":"done"}{"title":"addInputChange","message":"userName"}{"title":"loginOrigin","message":"loginMain"}',
        }
        response = self.session.post(self.login_url % (int(time.time()*1000)), data=data)
        response_json = json.loads(response.text.replace('&&&START&&&', ''))
        # 登录成功
        if response_json['code'] == 0:
            location_url = response_json['location']
            response = self.session.get(location_url)
            response = self.session.get(self.home_url)
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账户密码错误
        elif response_json['code'] in [70016]:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise ValueError(response_json['desc'])
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
        self.sign_url = 'https://account.xiaomi.com/pass/serviceLogin'
        self.login_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2?_dc=%s'
        self.home_url = 'https://www.mi.com/index.html'
        self.session.headers.update(self.headers)


'''移动端登录小米商城'''
class mieshopMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in mieshop in mobile mode'


'''扫码登录小米商城'''
class mieshopScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in mieshop in scanqr mode'


'''
Function:
    小米商城模拟登录
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
class mieshop():
    def __init__(self, **kwargs):
        self.info = 'login in mieshop'
        self.supported_modes = {
            'pc': mieshopPC(**kwargs),
            'mobile': mieshopMobile(**kwargs),
            'scanqr': mieshopScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in mieshop.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in mieshop.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)