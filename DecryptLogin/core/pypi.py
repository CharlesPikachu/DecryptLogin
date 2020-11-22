'''
Function:
    PyPi模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import re
import requests


'''PC端登录PyPi'''
class pypiPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in pypi in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得csrf_token参数
        response = self.session.get(self.login_url)
        csrf_token = re.findall(r'name="csrf_token" type="hidden" value="(.*?)"', response.text)[0]
        # 构造登录请求
        data = {
            'csrf_token': csrf_token,
            'username': username,
            'password': password
        }
        self.session.headers.update({'Referer': self.login_url})
        response = self.session.post(self.login_url, data=data, allow_redirects=False)
        response = self.session.get(self.projects_url)
        self.session.headers.update({'Referer': self.projects_url})
        response = self.session.get(self.currentuser_url)
        csrf_token = re.findall(r'name="csrf_token" type="hidden" value="(.*?)"', response.text)[0]
        # 登录成功
        if (response.status_code == 200) and (username in response.text):
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username, 'csrf_token': csrf_token}
            return infos_return, self.session
        # 登录失败
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        }
        self.login_url = 'https://pypi.org/account/login/'
        self.projects_url = 'https://pypi.org/manage/projects/'
        self.currentuser_url = 'https://pypi.org/_includes/current-user-indicator/'
        self.session.headers.update(self.headers)


'''移动端登录PyPi'''
class pypiMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in pypi in mobile mode'


'''扫码登录PyPi'''
class pypiScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in pypi in scanqr mode'


'''
Function:
    PyPi模拟登录
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
class pypi():
    def __init__(self, **kwargs):
        self.info = 'login in pypi'
        self.supported_modes = {
            'pc': pypiPC(**kwargs),
            'mobile': pypiMobile(**kwargs),
            'scanqr': pypiScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in pypi.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in pypi.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)