'''
Function:
    天翼模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-09
'''
import os
import time
import requests
from ..utils import removeImage, saveImage, showImage


'''PC端登录天翼'''
class eSurfingPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in eSurfing in pc mode'


'''移动端登录天翼'''
class eSurfingMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in eSurfing in mobile mode'


'''扫码登录天翼'''
class eSurfingScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in eSurfing in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获取登录二维码
        response = self.session.post(self.getUUID_url, data={'appId': 'E_189'})
        uuidinfos = response.json()
        headers = self.headers.copy()
        headers.update({
            'lt': 'EE4F0927B780B55FB0E9B7EF6176CD0F37B44514637133ADC02F91771B957966E51A36872AED12D33F449F0C06B90313ED309E1A5FC612D0D57D6839E1B735E463A62C77A59426D1F04E592A72AD4144A026221F',
            'origin': 'https://open.e.189.cn',
            'referer': 'https://open.e.189.cn/api/logbox/separate/index.html?appId=E_189&lt=EE4F0927B780B55FB0E9B7EF6176CD0F37B44514637133ADC02F91771B957966E51A36872AED12D33F449F0C06B90313ED309E1A5FC612D0D57D6839E1B735E463A62C77A59426D1F04E592A72AD4144A026221F&reqId=a6797952a8574c91bf8d4f1b1659829b',
            'reqid': 'a6797952a8574c91bf8d4f1b1659829b',
        })
        params = {
            'uuid': uuidinfos['uuid'],
            'REQID': headers['reqid'],
        }
        response = self.session.get(self.image_url, params=params)
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.png'))
        showImage(os.path.join(self.cur_path, 'qrcode.png'))
        # 检测二维码状态
        data = {
            'appId': 'E_189',
            'encryuuid': uuidinfos['encryuuid'],
            'date': time.strftime("%Y-%m-%d%H:%M:%S", time.localtime())+'23',
            'uuid': uuidinfos['uuid'],
            'returnUrl': 'https://e.189.cn/user/loginMiddle.do?returnUrlMid=https://e.189.cn/user/index.do',
            'clientType': '1',
            'timeStamp': int(time.time() * 1000),
            'cb_SaveName': '0',
            'isOauth2': 'false',
            'state': '',
            'paramId': 'E8FCE2B85E8A264AB7465122C6D900439CADFDD57D4D23F797712AD5E14D734E7FC3530329DECB73',
        }
        while True:
            response = self.session.post(self.qrcodeLoginState_url, data=data, headers=headers)
            response_json = response.json()
            if response_json['status'] in [-106, -11002]:
                time.sleep(1)
                continue
            elif response_json['status'] in [0]:
                break
            else:
                raise RuntimeError(response_json)
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.png'))
        response = self.session.get(response_json['redirectUrl'])
        headers = self.headers.copy()
        headers.update({
            'referer': 'https://e.189.cn/user/index.do'
        })
        response = self.session.get(self.level_url, headers=headers)
        response_json = response.json()
        username = response_json['hideMobile']
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        self.getUUID_url = 'https://open.e.189.cn/api/logbox/oauth2/getUUID.do'
        self.image_url = 'https://open.e.189.cn/api/logbox/oauth2/image.do'
        self.qrcodeLoginState_url = 'https://open.e.189.cn/api/logbox/oauth2/qrcodeLoginState.do'
        self.level_url = 'https://e.189.cn/user/safe/level.do'
        self.session.headers.update(self.headers)


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
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
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