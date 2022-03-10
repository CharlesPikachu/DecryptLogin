'''
Function:
    拉钩网模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-30
'''
import os
import re
import time
import hashlib
import requests
from ..utils.misc import *


'''PC端登录拉钩网'''
class lagouPC():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in lagou in pc mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 是否需要验证码的flag
        is_need_captcha = False
        while True:
            # 需要验证码
            if is_need_captcha:
                response = self.session.get(self.vcode_url.format(time.time()), headers=self.headers)
                saveImage(response.content, os.path.join(self.cur_path, 'captcha.jpg'))
                if crack_captcha_func is None:
                    showImage(os.path.join(self.cur_path, 'captcha.jpg'))
                    captcha = input('Input the captcha: ')
                else:
                    captcha = crack_captcha_func(os.path.join(self.cur_path, 'captcha.jpg'))
                removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
            # 提取动态token构造登录请求头
            anit_forge = self.__getAnitForge()
            login_headers = self.headers.copy()
            login_headers.update(anit_forge)
            # 获得密码密文
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
            password = 'veenike' + password + 'veenike'
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
            # 请求login_url
            data = {
                'isValidate': 'true',
                'username': username,
                'password': password,
                'request_form_verifyCode': '',
                'submit': '',
                'challenge': self.__getChallenge()
            }
            if is_need_captcha:
                data['request_form_verifyCode'] = captcha
            response = self.session.post(self.login_url, data=data, headers=login_headers)
            response_json = response.json()
            # 登录成功
            if response_json['state'] == 1:
                self.__verifyTicket()
                print('[INFO]: Account -> %s, login successfully' % username)
                infos_return = {'username': username}
                infos_return.update(response_json)
                return infos_return, self.session
            # 需要验证码
            elif response_json['state'] == 10010:
                is_need_captcha = True
            # 账号或密码错误
            elif response_json['state'] in [201, 203, 220, 240, 241, 400]:
                raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
            # 其他原因
            else:
                raise RuntimeError(response_json.get('message'))
    '''获得X-Anit-Forge-Code和X-Anit-Forge-Token参数'''
    def __getAnitForge(self):
        response = self.session.get(self.home_url, headers=self.headers)
        token = re.findall(r"window.X_Anti_Forge_Token = '(.*?)';", response.text)[0]
        code = re.findall(r"window.X_Anti_Forge_Code = '(.*?)';", response.text)[0]
        anit_forge = {
            'X-Anit-Forge-Code': code,
            'X-Anit-Forge-Token': token
        }
        return anit_forge
    '''验证ticket'''
    def __verifyTicket(self):
        response = self.session.get(self.ticket_url, headers=self.verify_headers, allow_redirects=False)
        url = response.next.url
        url = re.sub('http://', 'https://', url)
        self.verify_headers['Host'] = 'www.lagou.com'
        response = self.session.get(url, headers=self.verify_headers, allow_redirects=False)
    '''获得challenge参数'''
    def __getChallenge(self):
        params = {'pt': '0', 'gt': '66442f2f720bfc86799932d8ad2eb6c7'}
        data = 'nLYvtlnNYdUU68IXi84sdryl9ucQ2skF5u8LBLKXarWE41fPrzcL7yxmf2fYN2XDG1CyhqjVaXyi2Q)3oBs537a1dNTMv4w)U5b23FFwHcWMk(3gtb8VHP7U0ltLOistf5IoI5Bt11GMavQSlQJ(ga)AsFh0wTLAC9yNwbdBfZExS0TT)Ojw010QuOFPQg2sj2jvTEER1LRMLHmQKR0KjWN)4Cq2o2WUzhwPy7sFFxJuCxUO)5377hbgo5tdjTOFHwgkUqZrY1lkmsPmexujXXIgpN9p2aa5OQ)iMRZ(p0zfuAnBYAEBOy6H6vSopUiWGeNg(IO(ppE7X0b6Zpul)GqoNs3nuVCdlamTyui5qKhr8fyFSgzxiYWamJ5xR8PbvM9XQLEPZnxqvL(2P3nuRwa4S8qTzbMTwN3fw)KvEXUC2iatqz4G6ExOcfcUbQtRp7I1fEgjNb7Y8DEAZwmqyBG0qUVc3moKM8KZrWLZxR14Wp8AaG3WzJ)s4z9ouViog8nAt1PI6xlPHWKazr7bH1mfpKYmz8z2k)TKYeQtG9XAjjWtab(dr5AsPjQk1njJmgAI(48Bh7pLzZwJIW93YAtExbuCHGauxyEU28ZrKrqTjlgqu7KeurQU5hu(DhlIdMkmRqI(xguC8GjkYAlXF7aOjSvDwkxLUrLEE44CBe2gGNEFn6uax6HhvcUHIRMtIq0BB5Va4i)hnTK)WzcH2jetHMn4KVgFykF8NTKpWIkt(qIhiW)V1DNlfbmQi0ZmpUbLyOnLX42cjxwFh5Rnxrq(4WsPVm(Y8Oz0WtPaniTrAE6hFrdXS8PKyyefa49QcTFDJr9nrCgv5bu1dg6m5jVvypdt7mKGRpy3DILQ)TZ0LX6OHBwl)4375P0X9QEXf6Dl4r9)0gNi(xSfT0FYLNJVzMfk)cNulnhOzjpDisiUu5oZHtAK0ue9BiFa40lwSXDmAHxm5DcCmkaK1eINzFTplJt9Gk5KcDxqJPCYhNX1gvXmLBpKRcgqXZmIWRU6nYmkF76WLImaEhN)HK4RYPiGCvUt3(23sAmuJoFyHEsmTLbq13KRWY0tUbKhJjcPlOJUHduT1aSiWalhY0GTfhTiHfAu09zqENSHxVMAxtzi8FVSSZfPP82eIOyphvu(gukLDRaARVVAB4QFfgAxPSDWjRAT28IkMd1SiPug(fuJ9M61l2PzMiNxfZ6TXCtgUvmkOHgIybDYdPM6PB4ObXbV2wQf0q939Mkm8eVNsMvNPRZ0b1oJo0AnCz1IsxFn4JfCpB8M328wtH)7ve1jOBB4KulYQlXJuI3HUCJoUU5I0V)xAZhRI)nX0cepkfkCMwOjKmIihoLXA3y2Z8p3r04s9NZc8ngBkdacFpqYtnR19EmDeMoKgay8PGQ)(zZf1hHhWXuZWXTXdyR)KDvRdlx9wjG2FhV95QAH3aG85Dxufapym)b6kWJzKFw(qmsSpvUwUDhVQN2lfeUjR27eb2JZ0WP1GkQfG4LZ1CJYrBcfTx3zLD))kwiq3ScaVbT)B1GVfXqEP68zeLs9J)xwU7NgsI(QKtNw7WpymPl(g(FmDmxzrAMarwdqdoG2)KJRX5Qjz)ke8VnU8A09PVsdEwWKtkXjMUbvB)7Z3OFFOA(2EoKwthpb(mMyiUghjLD9(JXfqGm2k4RVF8vATKIo7YGKgadiI5vwzs0EOdpChJVk5E7c3MMCiuUHm9axWXP0i0)PmW(ZxoiT0ZJvnyCCn60nwyjKHpp5nXnN2SKZS8WBliyhdc8RUqVRnZeh0pH27jiPUGXYkRiAuoKDzl8S6l3NWm6xPPQw1MbldzTqmMTUsOuoR5CBzlU)TJl2gCSRgE1j(ChpXGSUfUvuTwaGBFfKWyQWsWdSbcC2tSEF2WP4lSdgEntDioWtRFeGUNg8tlnswrkfS6JhgE7BgfC36H(X1fytovT3vuTwilxGIt2xWuD9iY1Qxf9CtgSvo7vJTWmYneAQEyOUyqwcF5e6un(GCrMa7sizPHqf)gPseC2CeCQH9anwH7ZHiLiMRznWM(mH1CJEt52ez)IeiVTaDFpy1oYhURRwGoxMU2MkqIkw4LBR59MuKpBUdS6kZWcr(GwZ7VBLE3GAsX8ndtwoLAmeifdRQIonF7L1qozAKBU7lyJM2oqYXs(7gLJZyIWmTXVskE8iAIXp)yRtajPfnTintzNxGHEKCyVZQrr0XBEvt3UtksAv9(1V2N8EBn7Hkb8VKw5u6BdFnc0dMQqgum(zQaTb(URg4(O9EmTXcQSpLTm4IRX(Pm)44ZYezGD(8BZoukh7Mhko6a1LizgNMdmizc)F9YBHLXXdwec1wK8OAnQcZt7rbVfIl6Vd3HqoQdcId8B)NiAT4YWhJM39jEYbgBVzBhunEFV8DjTVSqudgf009qrFN(xrIo(EP5Wo6fYmTd7X4NMjElvOOm(2SV00ftg7d7(oUwkCHcEvQieQSZe(lmxeuIS0UMLAJ0nlyfFvrf0wr2oTKek1wu0)p17viMriD8ONEOqY9bqsKZBhtiGxgzN3pTYlj3vYDMSbylh02H5iFn)efqRTD8s8amfw645BqAGI65uTRAeGLTTq6tAZex(Cfo4r21MQxKgkREGGhoky)3cKWA97jirImA..4f0ae6c11327e4367bff580c5b909a03039cf44f566fad8680886dd52987bd4956933bdd2376e53c282edd8a5b79e38d2d078bc9a1eb186462d24ed2bc4cba3b2eda457b80a6dd8b1394e159b1a2d72d2f500a2b2703e372ade0e97fd741d75d6f401801e1022fd8772a463a15ce646ca0d00efe04500dfddd33f46e037bdb20'
        response = requests.post(self.challenge_url, data=data, params=params)
        response_json = response.json()
        if response_json['status'] == 'success':
            challenge = response_json.get('challenge')
        else:
            raise RuntimeError('Get the param named challenge error, error info is %s' % response_json.get('error'))
        return challenge
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Referer': 'https://passport.lagou.com/login/login.html',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'passport.lagou.com',
            'Origin': 'https://passport.lagou.com'
        }
        self.verify_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Host': 'passport.lagou.com',
            'Referer': 'https://passport.lagou.com/login/login.html'
        }
        self.home_url = 'https://passport.lagou.com/login/login.html'
        self.login_url = 'https://passport.lagou.com/login/login.json'
        self.challenge_url = 'https://api.geetest.com/gt_judgement'
        self.vcode_url = 'https://passport.lagou.com/vcode/create?from=register&refresh={}'
        self.ticket_url = 'https://passport.lagou.com/grantServiceTicket/grant.html'


'''移动端登录拉钩网'''
class lagouMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in lagou in mobile mode'


'''扫码登录拉钩网'''
class lagouScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in lagou in scanqr mode'


'''
Function:
    拉钩网模拟登录
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
class lagou():
    def __init__(self, **kwargs):
        self.info = 'login in lagou'
        self.supported_modes = {
            'pc': lagouPC(**kwargs),
            'mobile': lagouMobile(**kwargs),
            'scanqr': lagouScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in lagou.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in lagou.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)