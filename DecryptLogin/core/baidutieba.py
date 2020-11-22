'''
Function:
    百度贴吧模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import os
import time
import json
import requests
from ..utils.misc import *


'''PC端登录百度贴吧'''
class baidutiebaPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in baidutieba in pc mode'


'''移动端登录百度贴吧'''
class baidutiebaMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in baidutieba in mobile mode'


'''扫码登录百度贴吧'''
class baidutiebaScanQR():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in baidutieba in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得登录二维码
        timestamp = str(int(time.time() * 1000))
        params = {
            'lp': 'pc',
            'qrloginfrom': 'pc',
            'apiver': 'v3',
            'tt': timestamp,
            'tpl': 'tb',
            '_': timestamp
        }
        response = self.session.get(self.getqrcode_url, params=params)
        imgurl = response.json()['imgurl']
        sign = response.json()['sign']
        response = self.session.get('https://%s' % imgurl)
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检测二维码状态
        while True:
            timestamp = str(int(time.time() * 1000))
            params = {
                'channel_id': sign,
                'tpl': 'tb',
                'apiver': 'v3',
                'callback': '',
                'tt': timestamp,
                '_': timestamp
            }
            response = self.session.get(self.unicast_url, params=params)
            response_json = json.loads(response.text.replace('(', '').replace(')', ''))
            # --二维码失效或请求有误
            if 'channel_v' not in response_json:
                raise RuntimeError('Fail to login, qrcode has expired or something error when fetching qrcode status')
            # --正在扫码
            elif json.loads(response_json['channel_v'])['status'] in [1]:
                pass
            # --扫码成功
            elif json.loads(response_json['channel_v'])['status'] in [0]:
                timestamp = str(int(time.time() * 1000))
                response_json = json.loads(response_json['channel_v'])
                params = {
                    'v': timestamp,
                    'bduss': response_json['v'],
                    'u': 'https://tieba.baidu.com/index.html',
                    'loginVersion': 'v4',
                    'qrcode': '1',
                    'tpl': 'tb',
                    'apiver': 'v3',
                    'tt': timestamp,
                    'alg': 'v1',
                    'time': timestamp[10:]
                }
                response = self.session.get(self.login_url, params=params)
                response.encoding = 'utf-8'
                print(response.text)
                response_json = json.loads(response.text.replace("'", '"').replace('\\', ''))
                self.session.get(self.crossdomain_url+'?bdu=%s&t=%s' % (response_json['data']['hao123Param'], timestamp))
                response = self.session.get(self.userinfo_url)
                response_json['userinfo'] = response.json()
                username = response_json['userinfo']['data']['user_name_show']
                break
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        self.getqrcode_url = 'https://passport.baidu.com/v2/api/getqrcode'
        self.unicast_url = 'https://passport.baidu.com/channel/unicast'
        self.login_url = 'https://passport.baidu.com/v3/login/main/qrbdusslogin'
        self.crossdomain_url = 'https://user.hao123.com/static/crossdomain.php'
        self.userinfo_url = 'https://tieba.baidu.com/f/user/json_userinfo'


'''
Function:
    百度贴吧模拟登录
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
class baidutieba():
    def __init__(self, **kwargs):
        self.info = 'login in baidutieba'
        self.supported_modes = {
            'pc': baidutiebaPC(**kwargs),
            'mobile': baidutiebaMobile(**kwargs),
            'scanqr': baidutiebaScanQR(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in baidutieba.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in baidutieba.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)