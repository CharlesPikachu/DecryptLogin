'''
Function:
    京东模拟登录
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
from urllib.parse import unquote


'''PC端登录京东'''
class jingdongPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in jingdong in pc mode'


'''移动端登录京东'''
class jingdongMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in jingdong in mobile mode'


'''扫码登录京东'''
class jingdongScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in jingdong in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获取二维码
        response = self.session.get(self.qrshow_url.format(int(time.time()*1000)))
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检测二维码状态
        token = self.session.cookies.get('wlfstk_smdl')
        while True:
            response = self.session.get(self.token_url.format(token))
            response_json = json.loads(response.text[2: -1])
            # --扫码成功
            if response_json['code'] == 200:
                ticket = response_json['ticket']
                response = self.session.get(self.ticket_url.format(ticket))
                response_json = response.json()
                if not response_json['returnCode']:
                    response = self.session.get(response_json['url'])
                username = self.session.cookies.get('pin', '')
                nickname = unquote(self.session.cookies.get('unick', ''))
                break
            # --等待扫码以及正在扫码
            elif response_json['code'] in [201, 202]:
                pass
            # --二维码过期
            elif response_json['code'] == 203:
                raise RuntimeError('Fail to login, qrcode has expired')
            # --其他情况
            else:
                raise RuntimeError(response_json['msg'])
            time.sleep(1)
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        print('[INFO]: Account -> %s, login successfully' % nickname)
        infos_return = {'username': username, 'nickname': nickname}
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
        }
        self.qrshow_url = 'https://qr.m.jd.com/show?appid=133&size=147&t={}'
        self.token_url = 'https://qr.m.jd.com/check?callback=a&isNewVersion=1&_format_=json&appid=133&token={}'
        self.ticket_url = 'https://passport.jd.com/uc/qrCodeTicketValidation?t={}'
        self.session.headers.update(self.headers)


'''
Function:
    京东模拟登录
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
class jingdong():
    def __init__(self, **kwargs):
        self.info = 'login in jingdong'
        self.supported_modes = {
            'pc': jingdongPC(**kwargs),
            'mobile': jingdongMobile(**kwargs),
            'scanqr': jingdongScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in jingdong.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in jingdong.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)