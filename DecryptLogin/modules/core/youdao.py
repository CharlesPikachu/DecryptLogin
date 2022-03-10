'''
Function:
    有道模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import requests
from hashlib import md5


'''PC端登录有道'''
class youdaoPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in youdao in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 模拟登录
        data = {
            'app': 'web',
            'tp': 'urstoken',
            'cf': '7',
            'fr': '1',
            'ru': 'http://www.youdao.com',
            'product': 'DICT',
            'type': '1',
            'um': 'true',
            'username': username,
            'password': md5(password.encode('utf-8')).hexdigest(),
            'agreePrRule': '1',
            'savelogin': '1'
        }
        response = self.session.post(self.login_url, headers=self.login_headers, data=data, allow_redirects=False)
        # 访问主页
        self.session.get(self.home_url)
        # 获取个人信息
        response = self.session.get(self.accountinfo_url, headers=self.info_headers)
        response_json = response.json()
        # 登录成功
        if response_json['msg'] == 'OK' and response_json['code'] == 0:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 登录失败
        elif response_json['code'] in [2035]:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他原因
        else:
            raise RuntimeError(response_json.get('msg'))
    '''初始化'''
    def __initialize(self):
        self.info_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Host': 'dict.youdao.com',
            'Referer': 'http://dict.youdao.com/wordbook/wordlist?keyfrom=dict2.index'
        }
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Host': 'logindict.youdao.com',
            'Origin': 'http://account.youdao.com',
            'Referer': 'http://account.youdao.com/login?service=dict'
        }
        self.home_url = 'http://dict.youdao.com/'
        self.accountinfo_url = 'http://dict.youdao.com/login/acc/query/accountinfo'
        self.login_url = 'https://logindict.youdao.com/login/acc/login'


'''移动端登录有道'''
class youdaoMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in youdao in mobile mode'


'''扫码登录有道'''
class youdaoScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in youdao in scanqr mode'


'''
Function:
    有道模拟登录
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
class youdao():
    def __init__(self, **kwargs):
        self.info = 'login in youdao'
        self.supported_modes = {
            'pc': youdaoPC(**kwargs),
            'mobile': youdaoMobile(**kwargs),
            'scanqr': youdaoScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in youdao.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in youdao.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)