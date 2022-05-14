'''
Function:
    网易云音乐自动签到
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from DecryptLogin import login
from DecryptLogin.modules.core.music163 import Cracker


'''网易云音乐自动签到'''
class NeteaseSignin():
    def __init__(self, username='charlespikachu'):
        self.username = username
        self.session = self.login()
        self.csrf = re.findall('__csrf=(.*?) for', str(self.session.cookies))[0]
        self.cracker = Cracker()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://music.163.com/discover',
            'Accept': '*/*'
        }
    '''外部调用'''
    def run(self):
        # 签到接口
        signin_url = 'https://music.163.com/weapi/point/dailyTask?csrf_token=' + self.csrf
        # 模拟签到(typeid为0代表APP上签到, 为1代表在网页上签到)
        typeids = [0, 1]
        for typeid in typeids:
            client_name = 'Web端' if typeid == 1 else 'APP端'
            # --构造请求获得响应
            data = {
                'type': typeid
            }
            data = self.cracker.get(data)
            response = self.session.post(signin_url, headers=self.headers, data=data)
            response_json = response.json()
            # --判断签到是否成功
            if response_json['code'] == 200:
                self.logging('账号%s在%s签到成功' % (self.username, client_name))
            else:
                self.logging('账号%s在%s签到失败, 原因: %s' % (self.username, client_name, response_json.get('msg')))
    '''模拟登录'''
    def login(self):
        client = login.Client()
        music163 = client.music163(reload_history=True)
        infos_return, session = music163.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')