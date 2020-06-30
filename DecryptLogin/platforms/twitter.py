'''
Function:
    推特模拟登录:
        --PC端: https://twitter.com/login
        --移动端暂不支持
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
更新日期:
    2020-06-19
'''
import re
import requests


'''
Function:
    推特模拟登录
Detail:
    -login:
        Input:
            --username: 用户名
            --password: 密码
            --mode: mobile/pc
            --crackvcFunc: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
            --proxies: 为requests.Session()设置代理
        Return:
            --infos_return: 用户名等信息
            --session: 登录后的requests.Session()
'''
class twitter():
    def __init__(self, **kwargs):
        self.info = 'twitter'
        self.session = requests.Session()
    '''登录函数'''
    def login(self, username, password, mode='mobile', crackvcFunc=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 移动端接口
        if mode == 'mobile':
            self.__initializeMobile()
            # 访问home_url获取authenticity_token
            res = self.session.get(self.home_url, headers=self.headers)
            authenticity_token = re.findall(r'<input name="authenticity_token" type="hidden" value="(.*?)"', res.text)[0]
            # 访问login_url进行模拟登录
            data = {
                        'authenticity_token': authenticity_token,
                        'session[username_or_email]': username,
                        'session[password]': password,
                        'remember_me': '1',
                        'wfa': '1',
                        'commit': 'Log in',
                        'ui_metrics': ''
                    }
            res = self.session.post(self.login_url, headers=self.login_headers, data=data, allow_redirects=True)
            res_text = res.text
            # 需要安全验证
            if '/account/login_challenge?challenge_id' in res_text:
                challenge_response = input('This login is detected as suspicious activity, input the verify code sended to your binded email:')
                enc_user_id = re.findall(r'enc_user_id=(.*?)">', res_text)[0]
                challenge_id = re.findall(r'challenge_id=(.*?)&amp;', res_text)[0]
                data = {
                            'authenticity_token': authenticity_token,
                            'challenge_id': challenge_id,
                            'enc_user_id': enc_user_id,
                            'challenge_type': 'TemporaryPassword',
                            'platform': 'web',
                            'redirect_after_login': '/',
                            'remember_me': 'true',
                            'challenge_response': challenge_response
                        }
                res = self.session.post(self.challenge_url, headers=self.login_headers, data=data, allow_redirects=True)
                res_text = res.text.replace('&quot', '').replace(';', '')
            # 登录成功
            if res.status_code == 200:
                print('[INFO]: Account -> %s, login successfully...' % username)
                infos_return = {'username': username}
                return infos_return, self.session
            # 登录失败
            else:
                raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
        # PC端接口
        elif mode == 'pc':
            raise NotImplementedError
        # mode输入有误
        else:
            raise ValueError('Unsupport argument in twitter.login -> mode %s, expect <mobile> or <pc>...' % mode)
    '''初始化PC端'''
    def __initializePC(self):
        pass
    '''初始化移动端'''
    def __initializeMobile(self):
        self.headers = {
                        'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10'
                    }
        self.login_headers = {
                                'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10',
                                'origin': 'https://mobile.twitter.com',
                                'referer': 'https://mobile.twitter.com/login'
                            }
        self.home_url = 'https://mobile.twitter.com/session/new'
        self.login_url = 'https://mobile.twitter.com/sessions'
        self.challenge_url = 'https://mobile.twitter.com/account/login_challenge'


'''test'''
if __name__ == '__main__':
    twitter().login('', '')