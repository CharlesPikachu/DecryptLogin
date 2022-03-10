'''
Function:
    GitHub模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import re
import requests


'''PC端登录GitHub'''
class githubPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in github in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得token
        token = self.__getToken()
        # 模拟登录
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': token,
            'login': username,
            'password': password
        }
        response = self.session.post(self.post_url, headers=self.login_headers, data=data)
        if response.status_code == 200 and 'Sign in to GitHub · GitHub' not in response.text:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            return infos_return, self.session
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
    '''获取authenticity_token参数'''
    def __getToken(self):
        response = self.session.get(self.login_url)
        token = re.findall(r'authenticity_token.*?value="(.*?)"', response.text)[0]
        return token
    '''初始化'''
    def __initialize(self):
        self.login_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '196',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'github.com',
            'Origin': 'https://github.com',
            'Pragma': 'no-cache',
            'Referer': 'https://github.com/login',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'


'''移动端登录GitHub'''
class githubMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in github in mobile mode'


'''扫码登录GitHub'''
class githubScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in github in scanqr mode'


'''
Function:
    GitHub模拟登录
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
class github():
    def __init__(self, **kwargs):
        self.info = 'login in github'
        self.supported_modes = {
            'pc': githubPC(**kwargs),
            'mobile': githubMobile(**kwargs),
            'scanqr': githubScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in github.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in github.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)