'''
Function:
    坚果云模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-11-01
'''
import re
import requests


'''PC端登录坚果云'''
class jianguoyunPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in jianguoyun in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 访问getLoginCaptcha
        params = {'un': username}
        response = self.session.get(self.getLoginCaptcha_url, params=params)
        response_json = response.json()
        # 模拟登录
        data = {
            'login_email': username,
            'login_password': password,
            'remember_me': 'on',
            'login_dest_uri': '/d/home',
        }
        data.update(response_json)
        response = self.session.post(self.login_url, data=data)
        response = self.session.get(self.home_url)
        # 登录成功
        if username.split('@')[0] in response.text:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            page_info = re.findall(r'PageInfo=({.*?});', response.text.replace('\n', '').replace(' ', '').replace("'", ''))[0][1: -1]
            for item in page_info.split(','):
                key, value = item.split(':')[0], ':'.join(item.split(':')[1:])
                infos_return[key] = value
            return infos_return, self.session
        # 登录失败
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        print(response.text)
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'referer': 'https://www.jianguoyun.com/d/login'
        }
        self.getLoginCaptcha_url = 'https://www.jianguoyun.com/d/ajax/getLoginCaptcha'
        self.login_url = 'https://www.jianguoyun.com/d/login'
        self.home_url = 'https://www.jianguoyun.com/d/home'
        self.session.headers.update(self.headers)


'''移动端登录坚果云'''
class jianguoyunMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in jianguoyun in mobile mode'


'''扫码登录坚果云'''
class jianguoyunScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in jianguoyun in scanqr mode'


'''
Function:
    坚果云模拟登录
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
class jianguoyun():
    def __init__(self, **kwargs):
        self.info = 'login in jianguoyun'
        self.supported_modes = {
            'pc': jianguoyunPC(**kwargs),
            'mobile': jianguoyunMobile(**kwargs),
            'scanqr': jianguoyunScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in jianguoyun.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in jianguoyun.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)