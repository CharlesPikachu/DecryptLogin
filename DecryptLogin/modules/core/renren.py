'''
Function:
    人人网模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
import os
import time
import base64
import hashlib
import requests
from ..utils import removeImage, saveImage, showImage


'''PC端登录人人网'''
class renrenPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in renren in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 模拟登录
        is_need_captcha = False
        while True:
            if is_need_captcha:
                data = {
                    'appKey': 'bcceb522717c2c49f895b561fa913d10',
                    'callId': str(int(time.time() * 1000)),
                    'sessionKey': '',
                    'type': '1'
                }
                data['sign'] = self.getsign(data, data['appKey'])
                response = self.session.post(self.icode_url, json=data)
                response_json = response.json()
                saveImage(base64.b64decode(response_json['data']['imageBase64String']), os.path.join(self.cur_path, 'captcha.png'))
                if crack_captcha_func is None:
                    showImage(os.path.join(self.cur_path, 'captcha.png'))
                    captcha = input('Input the captcha: ')
                else:
                    captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.png'))
                removeImage(os.path.join(self.cur_path, 'captcha.png'))
                data = {
                    'user': username,
                    'password': hashlib.md5(password.encode('utf-8')).hexdigest(),
                    'appKey': 'bcceb522717c2c49f895b561fa913d10',
                    'callId': str(int(time.time() * 1000)),
                    'sessionKey': '',
                    'ick': response_json['data']['ick'],
                    'verifyCode': captcha,
                }
            else:
                data = {
                    'user': username,
                    'password': hashlib.md5(password.encode('utf-8')).hexdigest(),
                    'appKey': 'bcceb522717c2c49f895b561fa913d10',
                    'callId': str(int(time.time() * 1000)),
                    'sessionKey': '',
                }
            data['sig'] = self.getsign(data, data['appKey'])
            response = self.session.post(self.login_url, json=data)
            response_json = response.json()
            # 登录成功
            if response_json['errorCode'] == 0:
                print('[INFO]: Account -> %s, login successfully' % username)
                infos_return = {'username': username}
                infos_return.update(response_json)
                return infos_return, self.session
            # 登录失败, 尝试验证码
            elif (response_json['errorCode'] != 0) and (not is_need_captcha):
                is_need_captcha = True
            # 登录失败
            else:
                raise RuntimeError(response_json)
    '''获得签名'''
    def getsign(self, data, secret_key):
        sign = ''.join(f'{k}={data[k]}' for k in sorted(data.keys()))
        sign += secret_key
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        return sign
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'rrwapi.renren.com',
            'Origin': 'http://www.renren.com',
            'Referer': 'http://www.renren.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        self.home_url = 'http://renren.com/'
        self.login_url = 'https://rrwapi.renren.com/account/v1/loginByPassword'
        self.icode_url = 'https://rrwapi.renren.com/icode/v1/getBase64ImgCode'
        self.session.headers.update(self.headers)


'''移动端登录人人网'''
class renrenMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in renren in mobile mode'


'''扫码登录人人网'''
class renrenScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in renren in scanqr mode'


'''
Function:
    人人网模拟登录
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
class renren():
    def __init__(self, **kwargs):
        self.info = 'login in renren'
        self.supported_modes = {
            'pc': renrenPC(**kwargs),
            'mobile': renrenMobile(**kwargs),
            'scanqr': renrenScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in renren.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in renren.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)