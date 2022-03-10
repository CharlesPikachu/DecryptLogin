'''
Function:
    豆瓣模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-09
'''
import os
import re
import time
import requests
from ..utils import removeImage, saveImage, showImage


'''PC端登录豆瓣'''
class doubanPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in douban in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化cookie
        response = self.session.get(self.home_url)
        # 模拟登录
        data = {
            'ck': '',
            'name': username,
            'password': password,
            'remember': 'true',
            'ticket': ''
        }
        response = self.session.post(self.login_url, data=data)
        response_json = response.json()
        # 登录成功
        if response_json['status'] == 'success':
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号或密码错误
        elif response_json['status'] == 'failed' and response_json['message'] == 'unmatch_name_password':
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise RuntimeError(response_json.get('description'))
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Host': 'accounts.douban.com',
            'Origin': 'https://accounts.douban.com',
            'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony'
        }
        self.home_url = 'https://www.douban.com/'
        self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        self.session.headers.update(self.headers)


'''移动端登录豆瓣'''
class doubanMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in douban in mobile mode'


'''扫码登录豆瓣'''
class doubanScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in douban in scanqr mode'
        self.session = requests.Session()
        self.cur_path = os.getcwd()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 下载二维码
        data = {
            'ck': '',
            'ticket': 't03mZd7QmXsZo5ekor2XwtvV6ezR7hRDxYBnQwC3WIdK6uvfPq4iCOG-JFG-TkoTg6vWEueuKFIpJpP8_BJlG8XNlUUQCtoBmarY7ZS5DTTir1Z3i7pgpXsJQ**',
            'randstr': '@xGH',
            'tc_app_id': '2044348370',
        }
        response = self.session.post(self.qrcode_url, data=data)
        response_json = response.json()
        if response_json['status'] != 'success': raise RuntimeError(response_json)
        code, img_url = response_json['payload']['code'], response_json['payload']['img']
        headers = {'User-Agent': self.headers['User-Agent']}
        response = requests.get(img_url, headers=headers)
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.png'))
        showImage(os.path.join(self.cur_path, 'qrcode.png'))
        # 检测扫码状态
        params = {
            'ck': '',
            'code': code,
        }
        while True:
            response = self.session.get(self.status_url, params=params)
            response_json = response.json()
            login_status = response_json['payload']['login_status']
            if login_status in ['pending', 'scan']:
                time.sleep(1)
                continue
            elif login_status in ['login']:
                break
            else:
                raise RuntimeError(response_json)
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.png'))
        response = self.session.get(self.stat_url)
        response = self.session.get(self.home_url)
        username = re.findall(r'input name="nick" type="text" value="(.*?)"', response.text)[0]
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username, 'text': response.text}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Host': 'accounts.douban.com',
            'Origin': 'https://accounts.douban.com',
            'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony'
        }
        self.qrcode_url = 'https://accounts.douban.com/j/mobile/login/qrlogin_code'
        self.status_url = 'https://accounts.douban.com/j/mobile/login/qrlogin_status'
        self.stat_url = 'https://www.douban.com/stat.html?&action=login_success&platform=qrcode&callback=jsonp_00czy4260w6yer2'
        self.home_url = 'https://www.douban.com/'
        self.session.headers.update(self.headers)


'''
Function:
    豆瓣模拟登录
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
class douban():
    def __init__(self, **kwargs):
        self.info = 'login in douban'
        self.supported_modes = {
            'pc': doubanPC(**kwargs),
            'mobile': doubanMobile(**kwargs),
            'scanqr': doubanScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in douban.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in douban.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)