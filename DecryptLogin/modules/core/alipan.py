'''
Function:
    阿里云盘模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-07-19
'''
import os
import re
import time
import json
import qrcode
import base64
import requests
from ..utils import removeImage, saveImage, showImage


'''PC端登录阿里云盘'''
class alipanPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in alipan in pc mode'


'''移动端登录阿里云盘'''
class alipanMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in alipan in mobile mode'


'''扫码登录阿里云盘'''
class alipanScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in alipan in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获取登录二维码
        self.session.get('https://auth.aliyundrive.com/v2/oauth/authorize?client_id=25dzX3vbYqktVxyX&redirect_uri=https%3A%2F%2Fwww.aliyundrive.com%2Fsign%2Fcallback&response_type=code&login_type=custom&state=%7B%22origin%22%3A%22https%3A%2F%2Fwww.aliyundrive.com%22%7D')
        response = self.session.get('https://passport.aliyundrive.com/newlogin/qrcode/generate.do?appName=aliyun_drive&fromSite=52&appName=aliyun_drive&appEntrance=web&_csrf_token=8iPG8rL8zndjoUQhrQnko5&umidToken=27f197668ac305a0a521e32152af7bafdb0ebc6c&isMobile=false&lang=zh_CN&returnUrl=&hsiz=1d3d27ee188453669e48ee140ea0d8e1&fromSite=52&bizParams=&_bx-v=2.0.31')
        data = response.json()['content']['data']
        ck, t, code_content = data['ck'], data['t'], data['codeContent']
        # 保存并显示登录二维码
        qr = qrcode.QRCode(
            version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1,
        )
        qr.add_data(code_content)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检测二维码状态
        while True:
            response = self.session.post(self.qrcode_query_url, data={'ck': ck, 't': t})
            data = response.json()['content']['data']
            login_status = data['qrCodeStatus']
            if login_status in ['NEW', 'SCANED']:
                continue
            elif login_status in ['CONFIRMED']:
                break
            elif login_status in ['EXPIRED']:
                raise RuntimeError('Fail to login, qrcode has expired')
            else:
                raise RuntimeError(login_status)
            time.sleep(1)
        # token登录
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        pds_login_result = json.loads(base64.b64decode(data['bizExt']).decode('gbk'))['pds_login_result']
        access_token = pds_login_result['accessToken']
        headers = {
            'Referer': 'https://auth.aliyundrive.com/v2/oauth/authorize?client_id=25dzX3vbYqktVxyX&redirect_uri=https%3A%2F%2Fwww.aliyundrive.com%2Fsign%2Fcallback&response_type=code&login_type=custom&state=%7B%22origin%22%3A%22https%3A%2F%2Fwww.aliyundrive.com%22%7D'
        }
        response = self.session.post(self.token_login_url, json={'token': access_token}, headers=headers)
        code = re.findall(r'code=(.*?)\&', response.json()['goto'])[0]
        response = self.session.post(self.token_get_url, json={'code': code})
        refresh_token = response.json()['refresh_token']
        response = requests.post(self.refresh_url, json={'refresh_token': refresh_token})
        response_json = response.json()
        username = response_json['user_name']
        token, token_type, refresh_token, drive_id = response_json['access_token'], response_json['token_type'], response_json['refresh_token'], response_json['default_drive_id']
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'authorization': f'{token_type} {token}',
        }
        # 登录成功
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.qrcode_query_url = 'https://passport.aliyundrive.com/newlogin/qrcode/query.do?appName=aliyun_drive&fromSite=52&_bx-v=2.0.31'
        self.token_login_url = 'https://auth.aliyundrive.com/v2/oauth/token_login'
        self.token_get_url = 'https://api.aliyundrive.com/token/get'
        self.refresh_url = 'https://api.aliyundrive.com/token/refresh'


'''
Function:
    阿里云盘模拟登录
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
class alipan():
    def __init__(self, **kwargs):
        self.info = 'login in alipan'
        self.supported_modes = {
            'pc': alipanPC(**kwargs),
            'mobile': alipanMobile(**kwargs),
            'scanqr': alipanScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in alipan.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in alipan.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)