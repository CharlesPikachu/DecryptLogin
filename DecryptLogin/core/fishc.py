'''
Function:
    鱼C论坛模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import re
import requests
from hashlib import md5


'''PC端登录鱼C论坛'''
class fishcPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in fishc in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 模拟登录
        data = {
            'username': username,
            'password': md5(password.encode(encoding='utf-8')).hexdigest(),
            'quickforward': 'yes',
            'handlekey': 'ls'
        }
        response = self.session.post(self.login_url, headers=self.login_headers, data=data)
        # 登录失败
        if (u'登录失败' in response.text) or (u'密码错误次数过多' in response.text):
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 登录成功, 跳转到主页提取一些必要的信息
        response = self.session.get(self.home_url)
        uid = re.findall(r"discuz_uid = '(\d+)',", response.text)[0]
        nickname = re.findall(r'title="访问我的空间">(.*?)</a>', response.text)[0]
        print('[INFO]: Account -> %s, login successfully' % username)
        infos_return = {'username': username, 'nickname': nickname, 'uid': uid}
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Host': 'fishc.com.cn',
            'Origin': 'https://fishc.com.cn',
            'Referer': 'https://fishc.com.cn/'
        }
        self.home_url = 'https://fishc.com.cn/'
        self.login_url = 'https://fishc.com.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        self.session.headers.update(self.headers)


'''移动端登录鱼C论坛'''
class fishcMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in fishc in mobile mode'


'''扫码登录鱼C论坛'''
class fishcScanqr():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in fishc in scanqr mode'


'''
Function:
    鱼C论坛模拟登录
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
class fishc():
    def __init__(self, **kwargs):
        self.info = 'login in fishc'
        self.supported_modes = {
            'pc': fishcPC(**kwargs),
            'mobile': fishcMobile(**kwargs),
            'scanqr': fishcScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username, password, mode='pc', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in fishc.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in fishc.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)