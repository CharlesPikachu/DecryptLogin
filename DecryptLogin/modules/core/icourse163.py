'''
Function:
    中国大学MOOC模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
import re
import requests
from hashlib import md5


'''PC端登录中国大学MOOC'''
class icourse163PC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in icourse163 in pc mode'


'''移动端登录中国大学MOOC'''
class icourse163Mobile():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in icourse163 in mobile mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 模拟登录
        data = {
            'username': username,
            'passwd': md5(password.encode(encoding='utf-8')).hexdigest(),
            'mob-token': '',
        }
        response = self.session.post(self.login_url, data=data)
        response_json = response.json()
        if response_json['status']['code'] == 0:
            print('[INFO]: Account -> %s, login successfully' % username)
        else:
            raise RuntimeError(response_json['status'].get('message', '登录异常, 请重新尝试'))
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; PCT-AL10 Build/HUAWEIPCT-AL10)',
            'edu-app-channel': 'ucmooc_offical',
            'edu-app-type': 'android',
            'edu-app-version': '4.19.0',
        }
        self.login_url = 'http://www.icourse163.org/mob/logonByIcourse'
        self.session.headers.update(self.headers)


'''扫码登录中国大学MOOC'''
class icourse163Scanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in icourse163 in scanqr mode'


'''
Function:
    中国大学MOOC模拟登录
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
class icourse163():
    def __init__(self, **kwargs):
        self.info = 'login in icourse163'
        self.supported_modes = {
            'pc': icourse163PC(**kwargs),
            'mobile': icourse163Mobile(**kwargs),
            'scanqr': icourse163Scanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='mobile', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in icourse163.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in icourse163.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)