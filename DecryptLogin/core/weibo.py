'''
Function:
    微博模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-11-06
'''
import re
import rsa
import time
import random
import base64
import requests
import warnings
from ..utils.misc import *
from binascii import b2a_hex
warnings.filterwarnings('ignore')


'''PC端登录微博'''
class weiboPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in weibo in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 进行模拟登录
        is_need_captcha = False
        while True:
            # --是否需要验证码
            if is_need_captcha:
                params = {
                    'r': str(int(random.random()*100000000)),
                    's': '0'
                }
                response = self.session.get(self.pin_url, headers=self.headers, params=params)
                saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
                if crack_captcha_func is None:
                    showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                    captcha = input('Input the captcha: ')
                else:
                    captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
                removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
            # --请求prelogin_url
            su = base64.b64encode(username.encode('utf-8'))
            params = {
                'entry': 'weibo',
                'su': su,
                'rsakt': 'mod',
                'checkpin': '1',
                'client': 'ssologin.js(v1.4.19)',
                '_': str(int(time.time()*1000))
            }
            response = self.session.get(self.prelogin_url, headers=self.headers, params=params, verify=False)
            response_json = response.json()
            if response_json.get('msg', '') == 'system error':
                raise RuntimeError(response_json.get('msg'))
            nonce = response_json.get('nonce', '')
            pubkey = response_json.get('pubkey', '')
            rsakv = response_json.get('rsakv', '')
            servertime = response_json.get('servertime', '')
            # --请求ssologin_url
            publickey = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
            sp = rsa.encrypt((str(servertime)+'\t'+nonce+'\n'+password).encode('utf-8'), publickey)
            sp = b2a_hex(sp)
            data_post = {
                'entry': 'account',
                'gateway': '1',
                'from': '',
                'savestate': '30',
                'useticket': '0',
                'useticket': '1',
                'pagerefer': '',
                'vsnf': '1',
                'su': su,
                'service': 'account',
                'servertime': str(int(servertime)+random.randint(1, 20)),
                'nonce': nonce,
                'pwencode': 'rsa2',
                'rsakv': rsakv,
                'sp': sp,
                'sr': '1536 * 864',
                'encoding': 'UTF - 8',
                'cdult': '3',
                'domain': 'sina.com.cn',
                'prelt': '95',
                'returntype': 'TEXT'
            }
            if is_need_captcha:
                data_post['door'] = captcha
            response = self.session.post(self.ssologin_url, headers=self.headers, data=data_post, allow_redirects=False, verify=False)
            response_json = response.json()
            # --登录成功
            if response_json['retcode'] == '0':
                break
            # --用户名或密码错误
            elif response_json['retcode'] == '101':
                raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
            # --验证码错误
            elif response_json['retcode'] == '2070':
                raise RuntimeError('Account -> %s, fail to login, crack captcha error' % username)
            # --需要验证码
            elif response_json['retcode'] == '4049':
                is_need_captcha = True
            # --其他错误
            else:
                raise RuntimeError(response_json.get('reason', ''))
        ticket, ssosavestate = re.findall(r'ticket=(.*?)&ssosavestate=(.*?)"', response.text)[0]
        # 请求login_url和home_url, 进一步验证登录是否成功
        params = {
            'ticket': ticket,
            'ssosavestate': str(ssosavestate),
            'callback': 'sinaSSOController.doCrossDomainCallBack',
            'scriptId': 'ssoscript0',
            'client': 'ssologin.js(v1.4.19)',
            '_': str(int(time.time() * 1000))
        }
        params = '&'.join(['%s=%s' % (key, value) for key, value in params.items()])
        response = self.session.get(self.login_url+params, headers=self.headers, verify=False)
        uid = re.findall(r'"uniqueid":"(.*?)"', response.text)[0]
        response = self.session.get(self.home_url % uid, headers=self.headers, verify=False)
        if '我的首页' in response.text:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        else:
            raise RuntimeError('Account -> %s, fail to login, visit %s error' % (username, self.home_url % uid))
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.pin_url = 'https://login.sina.com.cn/cgi/pin.php'
        self.prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php?'
        self.ssologin_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self.login_url = 'https://passport.weibo.com/wbsso/login?'
        self.home_url = 'https://weibo.com/u/%s/home'


'''移动端登录微博'''
class weiboMobile():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in weibo in mobile mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 模拟登录
        data = {
            'username': username,
            'password': password,
            'savestate': '1',
            'r': 'https://m.weibo.cn/',
            'ec': '0',
            'pagerefer': 'https://m.weibo.cn/',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }
        response = self.session.post(self.login_url, headers=self.login_headers, data=data)
        response_json = response.json()
        # 登录成功
        if response_json['retcode'] in [20000000]:
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 用户名或密码错误
        elif response_json['retcode'] in [50011002]:
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 安全验证
        elif response_json['retcode'] in [50050011]:
            response = self.session.get(response_json['data']['errurl'])
            msg_type, tip_content, num_times = 'sms', 'You have to secondverify your account, please input the sms code your phone received: ', 0
            response_json = self.__sendverificationcode(username, msg_type=msg_type)
            while response_json['retcode'] not in [100000]:
                num_times += 1
                if num_times > 1: raise RuntimeError(response_json.get('msg'))
                if response_json['retcode'] in [8513]:
                    msg_type, tip_content = 'private_msg', 'You have to secondverify your account, please input the verification code in your private message: '
                    response_json = self.__sendverificationcode(username, msg_type=msg_type)
                    break
                else:
                    raise RuntimeError(response_json.get('msg'))
            code = input(tip_content)
            params = {
                'code': code,
                'msg_type': msg_type,
            }
            response = self.session.get(self.ajcheck_url, params=params)
            response_json = response.json()
            if response_json['retcode'] not in [100000]:
                raise RuntimeError(response_json.get('msg'))
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 其他错误
        else:
            raise RuntimeError(response_json['msg'])
    '''安全验证, 发送验证码'''
    def __sendverificationcode(self, username=None, msg_type='sms'):
        assert msg_type in ['sms', 'private_msg']
        params = {}
        if msg_type == 'sms':
            params = {
                'number': '1',
                'mask_mobile': username[:2] + '*******' + username[-2:],
            }
        params['msg_type'] = msg_type
        response = self.session.get(self.ajsend_url, params=params)
        return response.json()
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        }
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'
        }
        self.login_url = 'https://passport.weibo.cn/sso/login'
        self.ajsend_url = 'https://passport.weibo.cn/signin/secondverify/ajsend'
        self.ajcheck_url = 'https://passport.weibo.cn/signin/secondverify/ajcheck'
        self.session.headers.update(self.headers)


'''扫码登录微博'''
class weiboScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in weibo in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获取二维码
        response = self.session.get(self.qrcode_url.format(int(time.time() * 10000)))
        imageurl = re.findall(r'"image":"(.*?)"', response.text)[0].replace('\\', '')
        qrid = re.findall(r'"qrid":"(.*?)"', response.text)[0]
        response = self.session.get(imageurl)
        saveImage(response.content, os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检测二维码状态
        while True:
            params = {
                'entry': 'weibo',
                'qrid': qrid,
                'callback': 'STK_%s' % int(time.time() * 10000)
            }
            response = self.session.get(self.check_url, params=params)
            if 'succ' in response.text:
                response_json = eval(re.findall(r'"data":({.*?})', response.text)[0])
                break
            time.sleep(0.5)
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 模拟登录
        params = {
            'entry': 'weibo',
            'returntype': 'TEXT',
            'crossdomain': '1',
            'cdult': '3',
            'domain': 'weibo.com',
            'alt': response_json['alt'],
            'savestate': '30',
        }
        response = self.session.get(self.login_url, params=params)
        response_json = response.json()
        for url in response_json['crossDomainUrlList']:
            response = self.session.get(url, verify=False)
        # 登录成功
        response = self.session.get(self.home_url)
        print('[INFO]: Account -> %s, login successfully' % response_json.get('nick', username))
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.home_url = 'https://weibo.com'
        self.qrcode_url = 'https://login.sina.com.cn/sso/qrcode/image?entry=homepage&size=128&callback=STK_{}'
        self.check_url = 'https://login.sina.com.cn/sso/qrcode/check'
        self.login_url = 'http://login.sina.com.cn/sso/login.php'
        self.session.headers.update(self.headers)


'''
Function:
    微博模拟登录
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
class weibo():
    def __init__(self, **kwargs):
        self.info = 'login in weibo'
        self.supported_modes = {
            'pc': weiboPC(**kwargs),
            'mobile': weiboMobile(**kwargs),
            'scanqr': weiboScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in weibo.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in weibo.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)