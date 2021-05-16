'''
Function:
    推特模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2021-05-16
'''
import re
import random
import binascii
import requests


'''PC端登录推特'''
class twitterPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in twitter in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得authenticity_token
        authenticity_token = self.generatetoken()
        self.session.cookies.clear()
        self.session.get(self.login_url)
        # 模拟登录
        cookies = {'_mb_tk': authenticity_token}
        data = {
            'redirect_after_login': '/',
            'remember_me': '1',
            'authenticity_token': authenticity_token,
            'wfa': '1',
            'ui_metrics': '{}',
            'session[username_or_email]': username,
            'session[password]': password,
        }
        response = self.session.post(self.sessions_url, cookies=cookies, data=data)
        response_text = response.text
        # 需要安全验证
        if '/account/login_challenge?challenge_id' in response_text:
            challenge_response = input('This login is detected as suspicious activity, input the verification code sended to your binded email: ')
            enc_user_id = re.findall(r'enc_user_id=(.*?)">', response_text)[0]
            challenge_id = re.findall(r'challenge_id=(.*?)&amp;', response_text)[0]
            data = {
                'authenticity_token': authenticity_token,
                'challenge_id': challenge_id,
                'enc_user_id': enc_user_id,
                'challenge_type': 'TemporaryPassword',
                'platform': 'web',
                'redirect_after_login': '/',
                'remember_me': 'true',
                'challenge_response': challenge_response
            }
            response = self.session.post(self.challenge_url, headers=self.login_headers, data=data, allow_redirects=True)
            response_text = response.text.replace('&quot', '').replace(';', '')
        # 登录成功
        if response.status_code == 200:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            return infos_return, self.session
        # 登录失败
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
    '''生成token'''
    def generatetoken(self, size=16):
        token = random.getrandbits(size * 8).to_bytes(size, 'big')
        return binascii.hexlify(token).decode()
    '''初始化'''
    def __initialize(self):
        self.login_headers = {
            'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10',
            'origin': 'https://mobile.twitter.com',
            'referer': 'https://mobile.twitter.com/login'
        }
        self.login_url = 'https://twitter.com/login'
        self.sessions_url = 'https://twitter.com/sessions'
        self.challenge_url = 'https://mobile.twitter.com/account/login_challenge'


'''移动端登录推特'''
class twitterMobile():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in twitter in mobile mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 访问home_url获取authenticity_token
        try:
            response = self.session.get(self.home_url, headers=self.headers)
            authenticity_token = re.findall(r'<input name="authenticity_token" type="hidden" value="(.*?)"', response.text)[0]
        except:
            authenticity_token = self.generatetoken()
            self.session.cookies.clear()
            self.session.cookies.update({'_mb_tk': authenticity_token})
        # 访问login_url进行模拟登录
        data = {
            'authenticity_token': authenticity_token,
            'session[username_or_email]': username,
            'session[password]': password,
            'remember_me': '1',
            'wfa': '1',
            'commit': 'Log in',
            'ui_metrics': ''
        }
        response = self.session.post(self.login_url, headers=self.login_headers, data=data, allow_redirects=True)
        response_text = response.text
        # 需要安全验证
        if '/account/login_challenge?challenge_id' in response_text:
            challenge_response = input('This login is detected as suspicious activity, input the verification code sended to your binded email: ')
            enc_user_id = re.findall(r'enc_user_id=(.*?)">', response_text)[0]
            challenge_id = re.findall(r'challenge_id=(.*?)&amp;', response_text)[0]
            data = {
                'authenticity_token': authenticity_token,
                'challenge_id': challenge_id,
                'enc_user_id': enc_user_id,
                'challenge_type': 'TemporaryPassword',
                'platform': 'web',
                'redirect_after_login': '/',
                'remember_me': 'true',
                'challenge_response': challenge_response
            }
            response = self.session.post(self.challenge_url, headers=self.login_headers, data=data, allow_redirects=True)
            response_text = response.text.replace('&quot', '').replace(';', '')
        # 登录成功
        if response.status_code == 200:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            return infos_return, self.session
        # 登录失败
        else:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
    '''生成token'''
    def generatetoken(self, size=16):
        token = random.getrandbits(size * 8).to_bytes(size, 'big')
        return binascii.hexlify(token).decode()
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10'
        }
        self.login_headers = {
            'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10',
            'origin': 'https://mobile.twitter.com',
            'referer': 'https://mobile.twitter.com/login'
        }
        self.home_url = 'https://mobile.twitter.com/session/new'
        self.login_url = 'https://mobile.twitter.com/sessions'
        self.challenge_url = 'https://mobile.twitter.com/account/login_challenge'


'''扫码登录推特'''
class twitterScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in twitter in scanqr mode'


'''
Function:
    推特模拟登录
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
class twitter():
    def __init__(self, **kwargs):
        self.info = 'login in twitter'
        self.supported_modes = {
            'pc': twitterPC(**kwargs),
            'mobile': twitterMobile(**kwargs),
            'scanqr': twitterScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='mobile', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in twitter.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in twitter.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)