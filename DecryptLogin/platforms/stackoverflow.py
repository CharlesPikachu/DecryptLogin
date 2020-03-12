'''
Function:
	stackoverflow模拟登录
		--PC端: https://stackoverflow.com/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-12
'''
import re
import requests


'''
Function:
	stackoverflow模拟登录
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
class stackoverflow():
	def __init__(self, **kwargs):
		self.info = 'stackoverflow'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			raise NotImplementedError
		# PC端接口
		elif mode == 'pc':
			self.__initializePC()
			# 获得fkey
			fkey = self.__getFkey()
			# 模拟登录
			data = {
					'openid_identifier': '',
					'password': password,
					'fkey': fkey,
					'email': username,
					'oauth_server': '',
					'oauth_version': '',
					'openid_username': '',
					'ssrc': 'head'
				}
			params = {
					'ssrc': 'head',
					'returnurl': 'https://stackoverflow.com/'
				}
			res = self.session.post(self.login_url, data=data, params=params)
			# 登录成功
			if res.history:
				res = self.session.get(self.home_url)
				profile_url = 'https://stackoverflow.com' + re.findall(r'<a href="(.+)" class="my-profile', res.text)[0]
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username, 'fkey': fkey, 'profile_url': profile_url}
				return infos_return, self.session
			# 登录失败
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in stackoverflow.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''获得fkey值'''
	def __getFkey(self):
		params = {
					'ssrc': 'head',
					'returnurl': 'https://stackoverflow.com/'
				}
		res = self.session.get(self.login_url, params=params)
		fkey = re.findall(r'"fkey":"([^"]+)"', res.text)[0]
		return fkey
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
					}
		self.login_url = 'https://stackoverflow.com/users/login'
		self.home_url = 'https://stackoverflow.com/'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	stackoverflow().login('', '')