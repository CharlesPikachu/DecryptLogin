'''
Function:
    天翼云盘自动签到+抽奖
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import time
import json
import hmac
import random
import xmltodict
from urllib import parse
from DecryptLogin import login


'''自动签到+抽奖'''
class Cloud189Signin():
    def __init__(self, username, password):
        self.infos_return, self.session = self.login(username, password)
    '''外部调用'''
    def run(self):
        self.signin()
        self.draw()
    '''自动签到'''
    def signin(self):
        self.logging('开始自动签到')
        # 构造url
        params = {
            'rand': str(time.time() * 1000),
            'clientType': 'TELEANDROID',
            'version': '8.9.0',
            'model': 'Mi MIX3',
        }
        url = f'https://api.cloud.189.cn/mkt/userSign.action?{parse.urlencode(params)}'
        # 日期转换
        date = self.cst2gmt(int(float(params['rand'])))
        # 必要的信息
        infos = json.dumps(xmltodict.parse(self.infos_return['merge_info']))
        infos = json.loads(infos)
        # 签名
        sign = f'SessionKey={infos["userSession"]["sessionKey"]}&Operate=GET&RequestURI=/mkt/userSign.action&Date={date}'
        # 请求头
        headers = {
            'sessionkey': infos['userSession']['sessionKey'],
            'date': date,
            'signature': self.getsignhex(sign, infos['userSession']['sessionSecret']),
            'user-agent': 'Ecloud/8.9.0 (Mi MIX3; ; uc) Android/10',
            'host': parse.urlparse(url).hostname
        }
        # 开始请求
        response = self.session.get(url, headers=headers)
        response_json = json.dumps(xmltodict.parse(response.text))
        response_json = json.loads(response_json)
        # 判断签到是否成功
        if response_json.get('userSignResult', {}).get('result') in ['1', '-1']:
            self.logging(f"签到成功, {response_json['userSignResult']['resultTip']}")
        else:
            self.logging(f"签到失败, 错误码为{response_json['userSignResult']['result']}, {response_json['userSignResult']['resultTip']}")
    '''自动抽奖'''
    def draw(self):
        self.logging('开始自动抽奖')
        # 构造url
        url = 'https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=0'
        # 必要的信息
        infos = json.dumps(xmltodict.parse(self.infos_return['merge_info']))
        infos = json.loads(infos)
        # sso login以补充cookies
        params = {
            'sessionKey': infos['userSession']['sessionKey'],
            'sessionKeyFm': infos['userSession']['familySessionKey'],
            'appName': 'com.cn21.ecloud',
            'redirectUrl': url,
        }
        merge_url = f'https://m.cloud.189.cn/ssoLoginMerge.action?{parse.urlencode(params)}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Mi MIX3 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.66 Mobile Safari/537.36 clientCtaSdkVersion/v3.8.1 deviceSystemVersion/10 deviceSystemType/Android clientPackageName/com.cn21.ecloud clientPackageNameSign/1c71af12beaa24e4d4c9189f3c9ad576',
            'x-requested-with': 'com.cn21.ecloud',
            'host': parse.urlparse(merge_url).hostname
        }
        response = self.session.get(merge_url, headers=headers)
        # 构造请求头
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Mi MIX3 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.66 Mobile Safari/537.36 clientCtaSdkVersion/v3.8.1 deviceSystemVersion/10 deviceSystemType/Android clientPackageName/com.cn21.ecloud clientPackageNameSign/1c71af12beaa24e4d4c9189f3c9ad576',
            'x-requested-with': 'XMLHttpRequest',
            'referer': url,
        }
        # 构造url
        params = {
            'activityId': 'ACT_SIGNIN',
            'taskId': 'TASK_SIGNIN',
            'noCache': str(random.random())
        }
        url = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?{parse.urlencode(params)}'
        # 签到抽奖
        headers['host'] = parse.urlparse(url).hostname
        response = self.session.get(url, headers=headers)
        response_json = response.json()
        if 'prizeName' in response_json:
            self.logging(f'签到抽奖成功，奖品名称为{response_json["prizeName"]}')
        else:
            self.logging(f'签到抽奖失败, 错误码为{response_json["errorCode"]}')
        # 预请求
        url = 'https://m.cloud.189.cn/zhuanti/2016/sign/act.jsp?act=10'
        headers['host'] = parse.urlparse(url).hostname
        response = self.session.get(url, headers=headers)
        # 构造url
        params = {
            'activityId': 'ACT_SIGNIN',
            'taskId': 'TASK_SIGNIN_PHOTOS',
            'noCache': str(random.random())
        }
        url = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?{parse.urlencode(params)}'
        headers['referer'] = 'https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1'
        headers['host'] = parse.urlparse(url).hostname
        # 相册抽奖
        response = self.session.get(url, headers=headers)
        response_json = response.json()
        if 'prizeName' in response_json:
            self.logging(f'相册抽奖成功，奖品名称为{response_json["prizeName"]}')
        else:
            self.logging(f'相册抽奖失败, 错误码为{response_json["errorCode"]}')
    '''cst to gmt'''
    def cst2gmt(self, millisecond):
        millisecond -= 28800 * 1000
        t = time.strftime('%a, %d %b %Y %X GMT', time.localtime(millisecond / 1000))
        t = t.replace(', 0', ', ')
        return t
    '''signature the data to hex'''
    def getsignhex(self, data, session_secret=None):
        key = bytes.fromhex('6665353733346337346332663936613338313537663432306233326463393935') if session_secret is None else session_secret.encode('utf-8')
        return hmac.new(key, data.encode('utf-8'), 'sha1').hexdigest()
    '''模拟登录'''
    def login(self, username, password):
        client = login.Client()
        cloud189 = client.cloud189(reload_history=True)
        infos_return, session = cloud189.login(username, password, 'mobile')
        return infos_return, session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')