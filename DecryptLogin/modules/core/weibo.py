'''
Function:
    微博模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
import os
import re
import time
import json
import requests
from ..utils import removeImage, showImage, saveImage


'''PC端登录微博'''
class weiboPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in weibo in pc mode'
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
            'ec': '1',
            'pagerefer': '',
            'entry': 'wapsso',
            'sinacnlogin': '1',
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
            response_json = self.__sendverificationcode(username, msg_type=msg_type, verification_page=response)
            while response_json['retcode'] not in [100000]:
                num_times += 1
                if num_times > 1: raise RuntimeError(response_json.get('msg'))
                if response_json['retcode'] in [8513]:
                    msg_type, tip_content = 'private_msg', 'You have to secondverify your account, please input the verification code in your private message: '
                    response_json = self.__sendverificationcode(username, msg_type=msg_type, verification_page=response)
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
            login_url = response_json['data']['url']
            self.session.get(login_url)
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 其他错误
        else:
            raise RuntimeError(response_json['msg'])
    '''安全验证, 发送验证码'''
    def __sendverificationcode(self, username=None, msg_type='sms', verification_page=None):
        assert msg_type in ['sms', 'private_msg']
        params = {'msg_type': msg_type}
        if msg_type == 'sms':
            infos = json.loads(re.search(r'phoneList: JSON.parse\(\'([^\']+)\'\),', verification_page.text).group(1))
            params.update({
                'number': infos[0]['number'],
                'mask_mobile': infos[0]['maskMobile'],
            })
        else:
            self.session.get('https://passport.weibo.cn/signin/secondverify/index', params={'way': 'private_msg'})
        response = self.session.get(self.ajsend_url, params=params)
        return response.json()
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        }
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'Content': 'application/x-www-form-urlencoded',
            'Origin': 'https://passport.sina.cn',
            'Referer': 'https://passport.sina.cn/signin/signin'
        }
        self.login_url = 'https://passport.sina.cn/sso/login'
        self.ajsend_url = 'https://passport.weibo.cn/signin/secondverify/ajsend'
        self.ajcheck_url = 'https://passport.weibo.cn/signin/secondverify/ajcheck'
        self.session.headers.update(self.headers)


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
            'ec': '1',
            'pagerefer': '',
            'entry': 'wapsso',
            'sinacnlogin': '1',
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
            response_json = self.__sendverificationcode(username, msg_type=msg_type, verification_page=response)
            while response_json['retcode'] not in [100000]:
                num_times += 1
                if num_times > 1: raise RuntimeError(response_json.get('msg'))
                if response_json['retcode'] in [8513]:
                    msg_type, tip_content = 'private_msg', 'You have to secondverify your account, please input the verification code in your private message: '
                    response_json = self.__sendverificationcode(username, msg_type=msg_type, verification_page=response)
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
            login_url = response_json['data']['url']
            self.session.get(login_url)
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 其他错误
        else:
            raise RuntimeError(response_json['msg'])
    '''安全验证, 发送验证码'''
    def __sendverificationcode(self, username=None, msg_type='sms', verification_page=None):
        assert msg_type in ['sms', 'private_msg']
        params = {'msg_type': msg_type}
        if msg_type == 'sms':
            infos = json.loads(re.search(r'phoneList: JSON.parse\(\'([^\']+)\'\),', verification_page.text).group(1))
            params.update({
                'number': infos[0]['number'],
                'mask_mobile': infos[0]['maskMobile'],
            })
        else:
            self.session.get('https://passport.weibo.cn/signin/secondverify/index', params={'way': 'private_msg'})
        response = self.session.get(self.ajsend_url, params=params)
        return response.json()
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        }
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'Content': 'application/x-www-form-urlencoded',
            'Origin': 'https://passport.sina.cn',
            'Referer': 'https://passport.sina.cn/signin/signin'
        }
        self.login_url = 'https://passport.sina.cn/sso/login'
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
        params = {
            'entry': 'weibo',
            'size': '180',
            'callback': str(int(time.time() * 1000)),
        }
        response = self.session.get(self.qrcode_url, params=params)
        response_json = json.loads(response.text.split('(')[-1].split(')')[0])
        qrid = response_json['data']['qrid']
        imageurl = 'https:' + response_json['data']['image']
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
            response_json = json.loads(response.text.split('(')[-1].split(')')[0])
            if response_json['retcode'] in [20000000]: break
            time.sleep(0.5)
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 模拟登录
        params = {
            'entry': 'weibo',
            'returntype': 'TEXT',
            'crossdomain': '1',
            'cdult': '3',
            'domain': 'weibo.com',
            'alt': response_json['data']['alt'],
            'savestate': '30',
            'callback': 'STK_' + str(int(time.time() * 1000)),
        }
        response = self.session.get(self.login_url, params=params)
        response_json = json.loads(response.text.split('(')[-1].split(')')[0])
        response_json['crossDomainUrlList'][0] = response_json['crossDomainUrlList'][0] + '&action=login'
        for url in response_json['crossDomainUrlList']:
            response = self.session.get(url)
        # 登录成功
        response = self.session.get(self.home_url)
        print('[INFO]: Account -> %s, login successfully' % response_json.get('nick', username))
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'Referer': 'https://mail.sina.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
        self.home_url = 'https://weibo.com'
        self.qrcode_url = 'https://login.sina.com.cn/sso/qrcode/image'
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