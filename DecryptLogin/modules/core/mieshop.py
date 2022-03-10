'''
Function:
    小米商城模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import re
import time
import json
import hashlib
import warnings
import requests
warnings.filterwarnings('ignore')


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
        # 获得sign等值
        response = self.session.get(self.sign_url, verify=False)
        sign = re.findall(r'"_sign":"(.*?)",', response.text)[0]
        qs = re.findall(r'qs:"(.*?)",', response.text)[0]
        callback = re.findall(r'callback:"(.*?)"', response.text)[0]
        # 模拟登录
        data = {
            '_json': 'true',
            'callback': callback,
            'sid': 'mi_eshop',
            'qs': qs,
            '_sign': sign,
            'serviceParam': '{"checkSafePhone":false}',
            'user': username,
            'hash': hashlib.md5(password.encode(encoding='utf-8')).hexdigest().upper(),
            'cc': '',
            'log': ''
        }
        response = self.session.post(self.login_url % (int(time.time()*1000)), headers=self.login_headers, data=data)
        response_json = json.loads(response.text.replace('&&&START&&&', ''))
        # 登录成功
        if response_json['code'] == 0:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Host': 'account.xiaomi.com'
        }
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Host': 'account.xiaomi.com',
            'Origin': 'https://account.xiaomi.com',
            'Accept': '*/*',
            'Referer': 'https://account.xiaomi.com/pass/serviceLogin?sid=mi_eshop',
        }
        self.sign_url = 'https://account.xiaomi.com/pass/serviceLogin?sid=mi_eshop'
        self.login_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2?_dc=%s'
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