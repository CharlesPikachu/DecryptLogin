'''
Function:
    天翼模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-30
'''
import re
import rsa
import base64
import requests


'''PC端登录天翼'''
class eSurfingPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in eSurfing in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 请求home_url, 从网页提取请求unifyAccountLogin_url所需的参数
        response = self.session.get(self.home_url)
        sign, app_id, paras, format_, client_type, version = re.findall(r'sign=(.*?)&appId=(.*?)&paras=(.*?)&format=(.*?)&clientType=(.*?)&version=(.*?)">', response.text)[0]
        self.unifyAccountLogin_url = self.unifyAccountLogin_url.format(sign, app_id, paras, format_, client_type, version)
        # 请求unifyAccountLogin_url, 从网页提取登录所需的参数
        response = self.session.get(self.unifyAccountLogin_url)
        captcha_token = re.search(r"captchaToken' value='(.*?)'>", response.text).group(1)
        client_type, account_type, app_key = re.findall(r"clientType = '(.*?)'[\s\S]*?accountType = '(.*?)'[\s\S]*?appKey = '(.*?)'", response.text)[0]
        param_id = re.search(r'paramId = "(.*?)"', response.text).group(1)
        req_id = re.search(r'reqId = "(.*?)"', response.text).group(1)
        lt = re.search(r'lt = "(.*?)"', response.text).group(1)
        j_rsakey = re.findall(r'"j_rsaKey" value="(.*?)"', response.text)[0]
        # 请求loginSubmit_url进行模拟登录
        self.login_headers.update({'Referer': self.unifyAccountLogin_url, 'REQID': req_id, 'lt': lt})
        data = {
            'appKey': app_key,
            'accountType': account_type,
            'validateCode': '',
            'captchaToken': captcha_token,
            'returnUrl': 'https://e.189.cn/user/loginMiddle.do?returnUrlMid=https://e.189.cn/user/index.do',
            'mailSuffix': '',
            'dynamicCheck': 'FALSE',
            'clientType': client_type,
            'cb_SaveName': '1',
            'isOauth2': 'false',
            'state': '',
            'paramId': param_id,
            'userName': self.__encrypt(j_rsakey, username),
            'password': self.__encrypt(j_rsakey, password)
        }
        response = self.session.post(self.loginSubmit_url, headers=self.login_headers, data=data)
        response_json = response.json()
        # 登录成功
        if response_json['msg'] == u'登录成功' and response_json['result'] == 0:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号或密码错误
        elif response_json['result'] in [-51002, -17]:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise RuntimeError(response_json.get('msg'))
    '''天翼加密算法'''
    def __encrypt(self, j_rsakey, data):
        def int2char(index):
            return list('0123456789abcdefghijklmnopqrstuvwxyz')[index]
        def b64tohex(a):
            b64map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
            d, e, c = '', 0, 0
            for i in range(len(a)):
                if list(a)[i] != '=':
                    v = b64map.index(list(a)[i])
                    if 0 == e:
                        e = 1
                        d += int2char(v >> 2)
                        c = 3 & v
                    elif 1 == e:
                        e = 2
                        d += int2char(c << 2 | v >> 4)
                        c = 15 & v
                    elif 2 == e:
                        e = 3
                        d += int2char(c)
                        d += int2char(v >> 2)
                        c = 3 & v
                    else:
                        e = 0
                        d += int2char(c << 2 | v >> 4)
                        d += int2char(15 & v)
            if e == 1: d += int2char(c << 2)
            return d
        rsa_key = '-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----'.format(j_rsakey)
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode('utf-8'))
        data_encrypt = b64tohex((base64.b64encode(rsa.encrypt(data.encode('utf-8'), pubkey))).decode('utf-8'))
        return '{RSA}' + data_encrypt
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Host': 'open.e.189.cn',
            'Origin': 'https://open.e.189.cn',
            'Referer': '',
            'REQID': '',
            'lt': ''
        }
        self.home_url = 'https://e.189.cn/index.do'
        self.loginSubmit_url = 'https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do'
        self.unifyAccountLogin_url = 'https://open.e.189.cn/api/logbox/oauth2/unifyAccountLogin.do?sign={}&appId={}&paras={}&format={}&clientType={}&version={}'
        self.session.headers.update(self.headers)


'''移动端登录天翼'''
class eSurfingMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in eSurfing in mobile mode'


'''扫码登录天翼'''
class eSurfingScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in eSurfing in scanqr mode'


'''
Function:
    天翼模拟登录
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
class eSurfing():
    def __init__(self, **kwargs):
        self.info = 'login in eSurfing'
        self.supported_modes = {
            'pc': eSurfingPC(**kwargs),
            'mobile': eSurfingMobile(**kwargs),
            'scanqr': eSurfingScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in eSurfing.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in eSurfing.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)