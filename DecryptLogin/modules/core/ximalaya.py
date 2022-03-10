'''
Function:
    喜马拉雅模拟登录
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
import requests
from ..utils import saveImage, showImage, removeImage


'''PC端登录喜马拉雅'''
class ximalayaPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in ximalaya in pc mode'


'''移动端登录喜马拉雅'''
class ximalayaMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in ximalaya in mobile mode'


'''扫码登录喜马拉雅'''
class ximalayaScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in ximalaya in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获取二维码
        response = self.session.get(self.qrcode_url, verify=False)
        response_json = response.json()
        saveImage(base64.b64decode(response_json['img']), os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检测二维码状态
        qr_id = response_json['qrId']
        while True:
            response = self.session.get(self.check_url.format(qr_id, int(time.time() * 1000)), verify=False)
            response_json = response.json()
            # --扫码成功
            if response_json['ret'] in [0]:
                break
            # --等待/正在扫码
            elif response_json['ret'] in [32000]:
                pass
            # --其他原因
            else:
                raise RuntimeError(response_json.get('msg', 'something error'))
            time.sleep(0.5)
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        print('[INFO]: Account -> %s, login successfully' % response_json['mobileMask'] if response_json['mobileMask'] else response_json['uid'])
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        }
        self.qrcode_url = 'https://passport.ximalaya.com/web/qrCode/gen?level=L'
        self.check_url = 'https://passport.ximalaya.com/web/qrCode/check/{}/{}'
        self.session.headers.update(self.headers)


'''
Function:
    喜马拉雅模拟登录
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
class ximalaya():
    def __init__(self, **kwargs):
        self.info = 'login in ximalaya'
        self.supported_modes = {
            'pc': ximalayaPC(**kwargs),
            'mobile': ximalayaMobile(**kwargs),
            'scanqr': ximalayaScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in ximalaya.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in ximalaya.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)