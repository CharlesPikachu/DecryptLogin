'''
Function:
    虾米音乐模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import time
import json
import requests
from hashlib import md5


'''PC端登录虾米音乐'''
class xiamiPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in xiami in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得请求所需的token
        token = self.__getToken()
        # 模拟登录
        login_url = self.base_url.format(action=self.actions['login'])
        params = {
            'account': username,
            'password': md5(password.encode('utf-8')).hexdigest()
        }
        response = self.session.get(login_url, params=self.__xiamiSign(params, token))
        response_json = response.json()
        code, msg = response_json['ret'][0].split('::')
        # 登录成功
        if code == 'SUCCESS':
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号密码错误
        elif code in ['FAIL_BIZ_GLOBAL_WRONG_PARAMS', 'FAIL_BIZ_GLOBAL_APPLICATION_ERROR']:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他原因
        else:
            raise RuntimeError(msg)
    '''虾米签名'''
    def __xiamiSign(self, params, token='', access_token=None):
        appkey = '23649156'
        t = str(int(time.time() * 1000))
        request_str = {
            'header': {'appId': '200', 'platformId': 'h5'},
            'model': params
        }
        if access_token: request_str['header']['accessToken'] = access_token
        data = json.dumps({'requestStr': json.dumps(request_str)})
        sign = '%s&%s&%s&%s' % (token, t, appkey, data)
        sign = md5(sign.encode('utf-8')).hexdigest()
        params = {
            't': t,
            'appKey': appkey,
            'sign': sign,
            'data': data
        }
        return params
    '''获得请求所需的token'''
    def __getToken(self):
        action = self.actions['getsongdetail']
        url = self.base_url.format(action=action)
        params = {'songId': '1'}
        response = self.session.get(url, params=self.__xiamiSign(params))
        cookies = response.cookies.get_dict()
        return cookies['_m_h5_tk'].split('_')[0]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Referer': 'http://h.xiami.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        self.base_url = 'https://h5api.m.xiami.com/h5/{action}/1.0/'
        self.actions = {
            'getsongdetail': 'mtop.alimusic.music.songservice.getsongdetail',
            'login': 'mtop.alimusic.xuser.facade.xiamiuserservice.login',
            'getuserinfobyuserid': 'mtop.alimusic.xuser.facade.xiamiuserservice.getuserinfobyuserid'
        }
        self.session.headers.update(self.headers)


'''移动端登录虾米音乐'''
class xiamiMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in xiami in mobile mode'


'''扫码登录虾米音乐'''
class xiamiScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in xiami in scanqr mode'


'''
Function:
    虾米音乐模拟登录
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
class xiami():
    def __init__(self, **kwargs):
        self.info = 'login in xiami'
        self.supported_modes = {
            'pc': xiamiPC(**kwargs),
            'mobile': xiamiMobile(**kwargs),
            'scanqr': xiamiScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in xiami.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in xiami.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)