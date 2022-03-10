'''
Function:
    12306模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
import os
import time
import json
import base64
import requests
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT
from ..utils import removeImage, saveImage, showImage


'''PC端登录12306'''
class zt12306PC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zt12306 in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得device信息
        response = self.session.get(self.device_url)
        response_json = response.json()
        url = base64.b64decode(response_json['id']).decode()
        response = self.session.get(url)
        response_json = response.text
        if response_json.find('callbackFunction') >= 0: response_json = response_json[18:-2]
        response_json = json.loads(response_json)
        self.session.cookies.update({
            'RAIL_EXPIRATION': response_json.get('exp'),
            'RAIL_DEVICEID': response_json.get('dfp'),
        })
        device_id = response_json.get('dfp')
        # 获得验证码
        self.sendsms(username)
        sms = input('Input the sms code: ')
        # 模拟登录
        data = {
            'sessionid': '',
            'sig': '',
            'if_check_slide_passcode_token': '',
            'scene': '',
            'checkMode': '0',
            'randCode': sms,
            'username': username,
            'password': self.encrypt(password),
            'appid': 'otn',
        }
        response = self.session.post(self.login_url, data=data)
        if response.json()['result_code'] != 0: raise RuntimeError(response.json())
        # uamtk
        response = self.session.post(self.uamtk_url, data={'appid': 'otn'})
        response_json = response.json()
        if str(response_json['result_code']) != '0': raise RuntimeError(response_json)
        apptk = response_json['newapptk']
        response = self.session.post(self.uamauthclient_url, data={'tk': apptk})
        response_json = response.json()
        if str(response_json['result_code']) != '0': raise RuntimeError(response_json)
        infos_return = response_json
        username = infos_return['username']
        # 登录成功
        response = self.session.post(self.initMy12306Api_url)
        response_json = response.json()
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return.update(response_json)
        return infos_return, self.session
    '''加密密码'''
    def encrypt(self, password):
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(b'tiekeyuankp12306', SM4_ENCRYPT)
        encrypted_passwd = crypt_sm4.crypt_ecb(password.strip().encode())
        encrypted_passwd = base64.b64encode(encrypted_passwd).decode()
        return '@' + encrypted_passwd
    '''获得验证码'''
    def sendsms(self, username):
        cast_num = input('Input the last 4 digits of your ID card: ')
        data = {
            'appid': 'otn',
            'username': username,
            'castNum': cast_num
        }
        response = self.session.post(self.sms_url, data=data)
        response_json = response.json()
        if '获取手机验证码成功' not in response_json['result_message']:
            raise RuntimeError(response_json)
        return response_json
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        self.device_url = 'https://12306-rail-id-v2.pjialin.com/'
        self.sms_url = 'https://kyfw.12306.cn/passport/web/getMessageCode'
        self.login_url = 'https://kyfw.12306.cn/passport/web/login'
        self.uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        self.uamauthclient_url = 'https://kyfw.12306.cn/otn/uamauthclient'
        self.initMy12306Api_url = 'https://kyfw.12306.cn/otn/index/initMy12306Api'
        self.session.headers.update(self.headers)


'''移动端登录12306'''
class zt12306Mobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zt12306 in mobile mode'


'''扫码登录12306'''
class zt12306Scanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in zt12306 in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得device信息
        response = self.session.get(self.device_url)
        response_json = response.json()
        url = base64.b64decode(response_json['id']).decode()
        response = self.session.get(url)
        response_json = response.text
        if response_json.find('callbackFunction') >= 0: response_json = response_json[18:-2]
        response_json = json.loads(response_json)
        self.session.cookies.update({
            'RAIL_EXPIRATION': response_json.get('exp'),
            'RAIL_DEVICEID': response_json.get('dfp'),
        })
        device_id = response_json.get('dfp')
        # 下载二维码
        response = self.session.post(self.create_url, data={'appid': 'otn'})
        response_json = response.json()
        image, uuid = response_json['image'], response_json['uuid']
        saveImage(base64.b64decode(image), os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检查二维码扫码状态
        while True:
            data = {
                'RAIL_DEVICEID': device_id,
                'RAIL_EXPIRATION': str(int(time.time() * 1000)),
                'uuid': uuid,
                'appid': 'otn',
            }
            response = self.session.post(self.checkqr_url, data=data)
            response_json = response.json()
            if response_json['result_code'] in ['0', '1']:
                time.sleep(1)
                continue
            elif response_json['result_code'] in ['2']:
                break
            else:
                raise RuntimeError(response_json)
        # uamtk
        response = self.session.post(self.uamtk_url, data={'appid': 'otn'})
        response_json = response.json()
        if str(response_json['result_code']) != '0': raise RuntimeError(response_json)
        apptk = response_json['newapptk']
        response = self.session.post(self.uamauthclient_url, data={'tk': apptk})
        response_json = response.json()
        if str(response_json['result_code']) != '0': raise RuntimeError(response_json)
        infos_return = response_json
        username = infos_return['username']
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        response = self.session.post(self.initMy12306Api_url)
        response_json = response.json()
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        self.device_url = 'https://12306-rail-id-v2.pjialin.com/'
        self.create_url = 'https://kyfw.12306.cn/passport/web/create-qr64'
        self.checkqr_url = 'https://kyfw.12306.cn/passport/web/checkqr'
        self.uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        self.uamauthclient_url = 'https://kyfw.12306.cn/otn/uamauthclient'
        self.initMy12306Api_url = 'https://kyfw.12306.cn/otn/index/initMy12306Api'
        self.session.headers.update(self.headers)


'''
Function:
    12306模拟登录
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
class zt12306():
    def __init__(self, **kwargs):
        self.info = 'login in zt12306'
        self.supported_modes = {
            'pc': zt12306PC(**kwargs),
            'mobile': zt12306Mobile(**kwargs),
            'scanqr': zt12306Scanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in zt12306.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in zt12306.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)