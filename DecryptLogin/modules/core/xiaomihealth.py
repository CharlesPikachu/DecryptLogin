'''
Function:
    小米运动模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
import re
import requests


'''PC端登录小米运动'''
class xiaomihealthPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in xiaomihealth in pc mode'


'''移动端登录小米运动'''
class xiaomihealthMobile():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in xiaomihealth in mobile mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得access
        data = {
            'client_id': 'HuaMi',
            'password': password,
            'redirect_uri': 'https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html',
            'token': 'access',
        }
        response = self.session.post(self.registrations_url.format(username), data=data, allow_redirects=False)
        location = response.headers['Location']
        access = re.findall(r'(?<=access=).*?(?=&)', location)
        if len(access) < 1: raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        access = access[0]
        # 模拟登录
        data = {
            'app_name': 'com.xiaomi.hm.health',
            'app_version': '4.6.0',
            'code': access,
            'country_code': 'CN',
            'device_id': '2C8B4939-0CCD-4E94-8CBA-CB8EA6E613A1',
            'device_model': 'phone',
            'grant_type': 'access_token',
            'third_name': 'huami_phone'
        }
        response = self.session.post(self.login_url, data=data)
        response_json = response.json()
        if response_json['result'] == 'ok':
            print('[INFO]: Account -> %s, login successfully' % username)
        else:
            raise RuntimeError(response_json)
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'User-Agent': 'MiFit/4.6.0 (iPhone; iOS 14.0.1; Scale/2.00)'
        }
        self.registrations_url = 'https://api-user.huami.com/registrations/+86{}/tokens'
        self.login_url = 'https://account.huami.com/v2/client/login'
        self.session.headers.update(self.headers)


'''扫码登录小米运动'''
class xiaomihealthScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in xiaomihealth in scanqr mode'


'''
Function:
    小米运动模拟登录
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
class xiaomihealth():
    def __init__(self, **kwargs):
        self.info = 'login in xiaomihealth'
        self.supported_modes = {
            'pc': xiaomihealthPC(**kwargs),
            'mobile': xiaomihealthMobile(**kwargs),
            'scanqr': xiaomihealthScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='mobile', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in xiaomihealth.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in xiaomihealth.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)