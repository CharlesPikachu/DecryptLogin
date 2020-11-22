'''
Function:
    stackoverflow模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import re
import requests


'''PC端登录stackoverflow'''
class stackoverflowPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in stackoverflow in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得fkey
        fkey = self.__getFkey()
        # 模拟登录
        data = {
            'openid_identifier': '',
            'password': password,
            'fkey': fkey,
            'email': username,
            'oauth_server': '',
            'oauth_version': '',
            'openid_username': '',
            'ssrc': 'head'
        }
        params = {
            'ssrc': 'head',
            'returnurl': 'https://stackoverflow.com/'
        }
        response = self.session.post(self.login_url, data=data, params=params)
        # 登录成功
        if response.history:
            response = self.session.get(self.home_url)
            profile_url = 'https://stackoverflow.com' + re.findall(r'<a href="(.+)" class="my-profile', response.text)[0]
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username, 'fkey': fkey, 'profile_url': profile_url}
            return infos_return, self.session
        # 登录失败
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
    '''获得fkey值'''
    def __getFkey(self):
        params = {
            'ssrc': 'head',
            'returnurl': 'https://stackoverflow.com/'
        }
        response = self.session.get(self.login_url, params=params)
        fkey = re.findall(r'"fkey":"([^"]+)"', response.text)[0]
        return fkey
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        self.login_url = 'https://stackoverflow.com/users/login'
        self.home_url = 'https://stackoverflow.com/'
        self.session.headers.update(self.headers)


'''移动端登录stackoverflow'''
class stackoverflowMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in stackoverflow in mobile mode'


'''扫码登录stackoverflow'''
class stackoverflowScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in stackoverflow in scanqr mode'


'''
Function:
    stackoverflow模拟登录
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
class stackoverflow():
    def __init__(self, **kwargs):
        self.info = 'login in stackoverflow'
        self.supported_modes = {
            'pc': stackoverflowPC(**kwargs),
            'mobile': stackoverflowMobile(**kwargs),
            'scanqr': stackoverflowScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in stackoverflow.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in stackoverflow.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)