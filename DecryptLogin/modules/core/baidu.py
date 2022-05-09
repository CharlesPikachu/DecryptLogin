'''
Function:
    百度模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-05-09
'''
import os
import re
import time
import json
import uuid
import base64
import hashlib
import requests
from datetime import datetime
from Crypto.Cipher import AES
from urllib.parse import quote
from ..utils import saveImage, showImage, removeImage


'''PC端登录百度'''
class baiduPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in baidu in pc mode'


'''移动端登录百度'''
class baiduMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in baidu in mobile mode'


'''扫码登录百度'''
class baiduScanQR():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in baidu in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获得登录二维码
        timestamp = str(int(time.time() * 1000))
        callback = f'tangram_guid_{timestamp}'
        params = {
            'lp': 'pc',
            'qrloginfrom': 'pc',
            'gid': str(uuid.uuid4()).upper(),
            'callback': callback,
            'apiver': 'v3',
            'tt': timestamp,
            'tpl': 'mn',
            '_': timestamp
        }
        response = self.session.get(self.getqrcode_url, params=params)
        response_json = json.loads(re.search(r'\((.*?)\)', response.text)[1])
        imgurl, sign = response_json['imgurl'], response_json['sign']
        response = self.session.get('https://%s' % imgurl)
        qrcode_path = saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(qrcode_path)
        # 检测二维码状态
        while True:
            timestamp = str(int(time.time() * 1000))
            params = {
                'channel_id': sign,
                'tpl': 'mn',
                'gid': str(uuid.uuid4()).upper(),
                'callback': callback,
                'apiver': 'v3',
                'tt': timestamp,
                '_': timestamp
            }
            response = self.session.get(self.unicast_url, params=params)
            response_json = json.loads(re.search(r'\((.*?)\)', response.text)[1])
            # --二维码失效或请求有误
            if 'channel_v' not in response_json:
                raise RuntimeError('Fail to login in baidu, qrcode has expired or something error when fetching qrcode status')
            # --正在扫码
            elif json.loads(response_json['channel_v'])['status'] in [1]:
                pass
            # --扫码成功
            elif json.loads(response_json['channel_v'])['status'] in [0]:
                timestamp = str(int(time.time() * 1000))
                response_json = json.loads(response_json['channel_v'])
                params = {
                    'alg': 'v3',
                    'apiver': 'v3',
                    'bduss': response_json['v'],
                    'loginVersion': 'v4',
                    'qrcode': '1',
                    'time': timestamp[:-3],
                    'tpl': 'mn',
                    'tt': timestamp,
                    'u': 'https%3A%2F%2Fwww.baidu.com%2F',
                }
                params['sig'] = self.calcsign(params)
                params['shaOne'] = self.calcshaone()
                params['elapsed'] = 1234
                params['v'] = params['tt']
                params['callback'] = 'bd__cbs__odmford'
                response = self.session.get(self.login_url, params=params)
                for url in ['https://www.baidu.com/', 'http://index.baidu.com/api/SugApi/sug']:
                    response = self.session.get(url)
                response = self.session.post(self.abdr_url, data='''eyJkYXRhIjoiY2E0NzE1ZDhhNTgxZTljNmE0NzQxYjJkNTJmMzIwYjRkYWYwZGMzYzIzZTk5YmE0MGY1NzRjMjVkNzkyOGMxZjkxZDRlMDU0ZTY4Mzg3ZjEyZDYzNTQ1ODU2MDRhZGZkY2NmMzlmY2NhYjkzYTYyOGZiZjBhNzJlMDJmOWZmMjQ4NDdhM2E1MjA3NTViMjc4NjQ4YWM4OGYwZmI2NTNmYTZhNjgwZGNmZTM4YWEzOGRlMTVjZTg5NTYwZDE4YjY5Y2YyMjc4Mzg5YmMzNGVmMDBmNDMwZWUyMWNhYzE0MDI5MzJmM2JlNzIyNzAwYTliZmM1YjE3OGY1ZjgxYzA2MDFkNDliZjY2ZjM3ODJkOTkzMGNiNzJkYjE3MGVjZjY2MTEyM2NiMTM5MjlmNGIyOWVmYjljM2JlYjlkZjczZDYxNGY2YWViOWNhZjNiMjhmNjE2MDMxMjllYTkyNWY1MzU1ZDAxNjcyZWNjMDYxNTNkOWMzNTJiZTEwYzc2N2E0NjgxMjUzZDQ5MGExZTQxMDVlYWRmMzZlZDM1ZWMyNzY1NjU1ZmFmNjNkNTJjYjIyMzA1NDkzMjk2NWE1MTRiNTc2Mzk0MTMxNDJjNjMyZWFmZmI0NDFiNTVkMTViZjc3N2RiMGFhYzdlNWI5MWZkM2M3MWJkMjFkY2RiZTc5MzljZWI2OGYzOWNiODM4Zjk4NTMzNzFmOGZhNjI0MjQzY2YwYjIyOWJmZmZhYTA3Y2Y2YmVkZGVkZDZkZjgzYzAzZWM4N2Q3Y2Y5MWM4ZTc5Mjc2OWIxN2VjNWI4M2FiMzJiYWI0MTk3ZDUyOTllZWVmNjU0ZTJiN2NlNjVhYTNjNDMyODI3NTMwNWJhNzRhOGFhMmQ0M2VjMTIyNDU0N2U4ZjVkNDc2N2M1ODNhZjViYjAxMjZjYmEwMTI2ZmVjNzMzNjdlZTdjYjExMDgyYzljNTQ2ZDU0YzI4ZDcxMTY5NzBjMDlmYTAzMmI0YjliNTkyZTc5MWUyZDg4ZGEyZDViN2E2YWQwZWI3OTQ0MjBjMTVhMWNiNzk5NjRlNTQzNDkzNjA4YjY2OTc1ZDlmNjRlZDMyZDMyMjE0MWY4ODIzYzNjYmY3ODM5YmU4NDQ5MDYxNjJmNDJkMzkxYTExMzU4Y2MzMjMzOWRkMWY4ZGNlM2VkZjI3YTc1NmNhN2VkMDJiOTUwNjY1NGMwZTFjMDg1Mjk2OGFiYTVlMjhkZjk4MTMzNjczOGNhZTJiZWU5ODVmOTJkMGRiN2NiMDdiMDFjMDc0ZmMzZGMwZTdlMjBjYjUxNzM0MzdiNDUzYzNhYmU1NmQ5NDU4ZDA4MjIzZmQwMGUzNTYxNmI2Zjc0ODI0YWY0Mjc5ZjJiNWU3ZjNjMmUyYTkyMzhhMjFmMjdhY2Y0ZjM0NTYwZDQxNWEwNTFlYTk4YmFkOGVlY2RhMGFlZTg2MmJkMzQyZjJmZGUxNjg0OWM1NzliMGQ0YzdkOTZhNDM3ODMyYTI1M2YzMTAxZDQzODcwZjgxZjFkOWE5YTRjYTZkN2U1ZGMxZDk1ZjhjNDM0Y2RiN2VlNTViZTJjZjM5NGUyODI4NTY3M2IxMjBjMGE1YTdkMjViMjMyMmJmODVkYjY1ODJkZWQ2MzQ0MWFhNzM1NWE1ODgyMzZhMTlmOGY4YjU3MDUyMjA0OTA1NDZmZTc0NDY0ZWMwNzk2Y2JjMmQ0MzQ3MTI1NjA4ZDc2MDViOTYwMTJkMWI1ZTgzYTBmMzdmYmYxNWE2NTYyYTM1NWNiOTk5NTNjZjI0OWIzNGE2OGE5YWVhMTcyODhiODkwZmY0MjhkNWE0NmY3ZTc5YTE3ODYwNTY2YzAxODliNDVhZmFmZDNhNWNkNmYzOTc1NzkxODFiYjYyMzVjZjIyZGI4OTY3ZTI5OTA4ODQ4Yjg2YjgzMTc4YjExMTQ2ZDdmZjEwNTM4YzFmMGRlNjU5N2QyNWQwY2JlZjYyNTkzNjVhNWM4MDY5NDVmMDdmYTQzYWVjZDNkNzg1YzE0MjM5ODNhYTI3Zjk2MzIxZDhjMjc2NTU5MGQ1ZTU2NzU0MGRkODg0YjVmMWQ1MGUzYjM1Y2U5MGVmYmJiYjNjM2RiMTg1NzJjNmIwMTkxNjQxMzc5YzBlYjRkMGI4NTkwMzE0NzllMGEzODVmYzkzNDY3YzJjMzM2MDdjZGY1YzdiZWE4ZjM2ZTYyYWYwMDRkOTQ0N2EyNzcyMGYzNDIzNWRiZWMxOGYzNzNhZmQxMDBmNjlhODM4MTYxMTZhMmZmYzdkZDNlNmMxOWM4MzZmMDJkMzdhZjk4ZjE0MDkwMzJlZTNkZjE2MDU1N2FkZDAzYzdhODcwNmJiZmU0YTk2MDk4MzkyOGExOThhZWM5Yzk2ZWYzNzdjOWRmMDczMzM3ZGIxZTQxMzc5OGExNGRhZTA2M2Y4YjEyZWZkYjY4YmM2ODljY2ZmNTkxMGM1MTI0NzQzZjFlNzkzOGE5MDYwODc5MzgzOTY4NzE3ZTU0Y2I1MDc1NzJiNWI1MmQyM2E3MzU2NTViNWZlNDljMDEyZDE0MThkNmZlMzQxYWZmZTNkN2YzNGMwZDU2MTYzMDY0ODkyNmMwODc2YzJiMGMzZTRiZGQ4Y2ZlZjg0OTk2ZGFjNGIzNmRlODRlMzJmYjM4NTI1YThjMmFhNjljMDhkYmFmNTg5ZTdmNmRjMTkyMjMwZTIxZjgyYTcyNTk3YzJiNzFmNjFlMTVlNjQwYmZlNDhiZGY3MmJlZTMyYWFhMzQ0ZDNlYjRiM2VlZjgwMjYwNDA1ZTNhYTc3OGQxMmEzYmRkNzM2MzQ1NmViZjc1ZjUxNDQzZmU0MjIyYzYyNDM5YWJhNTBhYTBhNWU5ZTkwY2FmMmJmMGJhNjIzNDhjZWMyMjQyNTU5Njk1YWE2MTEyZDI2ZDA0NGMwNjI5YWJiMTc1MDU1ZjBmZGEwNjRlN2JlZGE1YmJiOWUxMzVhZDI4OWJlOWJmOWY2YTBiZTQyZWMzZTJiNjZjNmYxMWUzMmZmODE3ZGU0YTQ5OTVjYTg5MjM5OGI2MGJkMzJkNmUzY2QzNDRjYjc1ZWEzNjdiMDg4ZTdmOWQ0ZjVjZWE4NDQ2MTFhN2QxOWQ5NmRkMDZjYzYxMDJiZDAyZGIyYzNjNzU3YzUxZmRmNDI2M2UxYmE3MmYyZDliY2M0ZWQ0ZmE4ZDA3ZGM0MTAxYjllNmU2YzcwNzlhYTVlNmQwYWIxMjI2NWIyMDM2MmM4ODkzNWZmYTQ4OTMzZDNkZWFhMzUxYzM1YjEzZTI5OTQ1OWY0NzdkN2UzMmJkZDQxMjcwZWY1OTQ3NTY5MDYxYjMzZTMwNmQ1OWY3ZGJmOTZkM2MyNmM3YTc4NjdhMTczNTNjZThjYTUzN2JjNjZkZDkzZDdhODRiNzU4MGQ4ZTUyMmVkMWY1ZmE2MjEwYWRmZTM2NjM3NzRmNWQyMTM0MDgyNmRkYTAxMjM3MWZmY2JkZWRhZGYyOWRmMzIwZGY1MTc3ODU0MzkzNmFjNTZjOGUxZmNiMzZkOWMxZmY2ODNhMjE2ZjUxNzU1NjI0YWQ2YTcxYmViZGYxMjgwNzFkZWU4ZWJkMDE0YmIyZmVkYzdhYWNkY2FiM2Y4ODk1MTg0ZjQwYTdiNWI5ZmQ5NmQ3OWE2YzNmOWJkMzA3NDQ5MGQ3Zjg0MGE3NjVmOTFlNDFjZDE2MDBmYjQ0ODI5ODJmYzA2OTE0YzRlY2M2MzRhZWY1NjM4NDE4MDFjYjM0N2Q5YmU1NThkYmMzMjI1MzY5ODYyODkxMmNmNzVmNjlmOGM2ZDA1YjlkNWQ2ZmZlM2M4MWI0NDZiMWQ1Y2E3ZjVkYTg5NDRjZTcxYWU0OGNmMGJjMTNjNjVmZjAxMTIyZGFiZjcwMDJjMDM3ZDVkMmZjMzg0M2VhN2E4YWFkY2Q2ZTk4MjdkNGIyZDYwMDdiOWQyZWEwZTc0NTU3ODlmODUwNjJjMzMzMWM4YmVkYTQ3NjA2MjYxZmE1NGE1ODVjNjYzNDliYzkzODA0Y2NjYzRlMWI2NWI0OTM4ZjkwOThlYmVmZjU0YjhkYzVjZGRhNTllMjE3NjNhNDYyNzAxZTRlYzUwYmFmNzA4YjI1YzYzMzcxYmZhNmU0NjgiLCJrZXlfaWQiOiI5NWIyYzAzZGJhNWM0M2I0In0=''')
                response_json = json.loads(response.text)
                if isinstance(response_json['data'], dict):
                    shitong = '{}_{}_{}_{}_{}_{}_{}'.format(
                        response_json['data']['ver'],
                        response_json['key_id'],
                        response_json['data']['lid'],
                        response_json['data']['ret_code'],
                        response_json['data']['server_time'],
                        response_json['data']['ip'],
                        response_json['sign']
                    )
                    self.session.cookies.update({'__yjsv5_shitong': shitong})
                elif isinstance(response_json['data'], str):
                    shitong = '2_{}'.format(
                        base64.b64encode(quote('_'.join([response_json['data'], response_json['key_id'], response_json['sign']])).encode()).decode()
                    )
                    self.session.cookies.update({'__yjs_st': shitong})
                response = self.session.get(self.userinfo_url)
                response_json['userinfo'] = response.json()
                username = response_json['userinfo']['data']['user_name_show']
                break
        # 登录成功
        removeImage(qrcode_path)
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''计算shaone'''
    def calcshaone(self):
        timestamp = str(int(datetime.now().timestamp() * 1000))
        m5 = hashlib.md5(timestamp.encode()).hexdigest()
        return hashlib.sha1(m5.encode()).hexdigest()
    '''计算sign'''
    def calcsign(self, params):
        def paddingpkcs7(m):
            return m + chr(16 - len(m) % 16) * (16 - len(m) % 16)
        text = '&'.join([f'{key}={value}' for key, value in params.items()])
        m5 = hashlib.md5(text.encode()).hexdigest()
        insert_string = 'tnrstsms'
        final_text_start = ''.join([s + e for s, e in zip(m5[:8], insert_string)])
        final_text = final_text_start + m5[8:]
        aes = AES.new('moonshad8moonsh6'.encode(), AES.MODE_ECB)
        first_base64 = base64.b64encode(aes.encrypt(paddingpkcs7(final_text).encode()))
        return base64.b64encode(first_base64).decode()
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        self.getqrcode_url = 'https://passport.baidu.com/v2/api/getqrcode'
        self.unicast_url = 'https://passport.baidu.com/channel/unicast'
        self.login_url = 'https://passport.baidu.com/v3/login/main/qrbdusslogin'
        self.abdr_url = 'https://miao.baidu.com/abdr'
        self.userinfo_url = 'https://tieba.baidu.com/f/user/json_userinfo'
        self.session.headers.update(self.headers)


'''
Function:
    百度模拟登录
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
class baidu():
    def __init__(self, **kwargs):
        self.info = 'login in baidu'
        self.supported_modes = {
            'pc': baiduPC(**kwargs),
            'mobile': baiduMobile(**kwargs),
            'scanqr': baiduScanQR(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in baidu.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in baidu.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)