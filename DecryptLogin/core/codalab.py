'''
Function:
    CodaLab模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import re
import requests


'''PC端登录CodaLab'''
class codalabPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in codalab in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得csrfmiddlewaretoken参数
        response = self.session.get(self.token_url)
        csrfmiddlewaretoken = re.findall(r"name='csrfmiddlewaretoken' value='(.*?)'", response.text)[0]
        # 构造登录请求
        data = {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'login': username,
            'password': password,
            'remember': 'on',
            'next': '/'
        }
        self.session.headers.update({'Referer': self.token_url})
        response = self.session.post(self.login_url, data=data, allow_redirects=False)
        response = self.session.get(self.home_url)
        # 登录成功
        if (response.status_code == 200) and (username in response.text):
            print('[INFO]: Account -> %s, login successfully' % username)
            user_id = re.findall(r'user_id: (\d+),', response.text)[0]
            email = re.findall(r'email: "(.*?)",', response.text)[0]
            infos_return = {'username': username, 'user_id': user_id, 'email': email}
            return infos_return, self.session
        # 登录失败
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Host': 'competitions.codalab.org'
        }
        self.token_url = 'https://competitions.codalab.org/accounts/login/?next=/'
        self.home_url = 'https://competitions.codalab.org/'
        self.login_url = 'https://competitions.codalab.org/accounts/login/'
        self.session.headers.update(self.headers)


'''移动端登录CodaLab'''
class codalabMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in codalab in mobile mode'


'''扫码登录CodaLab'''
class codalabScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in codalab in scanqr mode'


'''
Function:
    CodaLab模拟登录
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
class codalab():
    def __init__(self, **kwargs):
        self.info = 'login in codalab'
        self.supported_modes = {
            'pc': codalabPC(**kwargs),
            'mobile': codalabMobile(**kwargs),
            'scanqr': codalabScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in codalab.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in codalab.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)