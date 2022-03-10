'''
Function:
    w3cschool模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import requests


'''PC端登录w3cschool'''
class w3cschoolPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in w3cschool in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化cookies
        self.session.get(self.home_url)
        # 模拟登录
        data = {
            'fromid': '',
            'username': username,
            'password': password,
            'remember': '1',
            'scode': ''
        }
        response = self.session.post(self.login_url, data=data)
        response_json = response.json()
        # 登录成功
        if response_json['statusCode'] == 200:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号或密码错误
        elif response_json['statusCode'] in [301]:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise RuntimeError(response_json.get('message'))
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.home_url = 'https://www.w3cschool.cn/login?refer=/'
        self.login_url = 'https://www.w3cschool.cn/checklogin_1'
        self.session.headers.update(self.headers)


'''移动端登录w3cschool'''
class w3cschoolMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in w3cschool in mobile mode'


'''扫码登录w3cschool'''
class w3cschoolScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in w3cschool in scanqr mode'


'''
Function:
    w3cschool模拟登录
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
class w3cschool():
    def __init__(self, **kwargs):
        self.info = 'login in w3cschool'
        self.supported_modes = {
            'pc': w3cschoolPC(**kwargs),
            'mobile': w3cschoolMobile(**kwargs),
            'scanqr': w3cschoolScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in w3cschool.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in w3cschool.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)