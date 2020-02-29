'''
Function:
	搜狐模拟登录:
		--PC端: http://www.sohu.com/
		--移动端: https://m.passport.sohu.com/app/login
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-29
'''
import time
import requests
from hashlib import md5


'''
Function:
	搜狐模拟登录
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
class sohu():
	def __init__(self, **kwargs):
		self.info = 'sohu'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='mobile', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			self.__initializeMobile()			
			# 访问app_login_url
			params = {
						'appid': 116001,
						'r': 'https://m.sohu.com/ucenter?_from=passport'
					}
			self.session.get(self.app_login_url, params=params)
			# 请求security_login_url
			data = {
					'userid': username,
					'password': md5(password.encode(encoding='utf-8')).hexdigest(),
					'appid': 116001
				}
			self.session.headers.update({
											'Accept': 'application/json',
											'Content-Type': 'application/x-www-form-urlencoded',
											'Origin': 'https://m.passport.sohu.com',
											'Referer': 'https://m.passport.sohu.com/app/login?appid=116001&r=https%3A%2F%2Fm.sohu.com%2Fucenter%3F_from%3Dpassport'
										})
			res = self.session.post(self.security_login_url.format(int(time.time()*1000)), data=data)
			res_json = res.json()
			# 登录成功
			if res_json.get('status') == 200 and res_json.get('message') == 'Success':
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				return infos_return, self.session
			# 账号或密码有误
			elif res_json.get('status') in [404, 459]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他原因
			else:
				raise RuntimeError(res_json.get('message'))
		# PC端接口
		elif mode == 'pc':
			self.__initializePC()
			# 请求home_url
			self.session.get(self.home_url)
			# 请求login_url
			data = {
					'userid': username,
					'password': md5(password.encode(encoding='utf-8')).hexdigest(),
					'persistentCookie': '1',
					'appid': '116005'
				}
			res = self.session.post(self.login_url, data=data)
			res_json = res.json()
			# 登录成功
			if res_json.get('status') == 200 and res_json.get('message') == 'Success':
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				return infos_return, self.session
			# 账号或密码有误
			elif res_json.get('status') in [404, 459]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他原因
			else:
				raise RuntimeError(res_json.get('message'))
		else:
			raise ValueError('Unsupport argument in sohu.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
							'origin': 'https://www.sohu.com',
							'upgrade-insecure-requests': '1',
							'referer': 'https://www.sohu.com/',
							'origin': 'https://www.sohu.com'
						}
		self.home_url = 'http://www.sohu.com/'
		self.login_url = 'https://v4.passport.sohu.com/i/login/116005'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		self.headers = {
						'Upgrade-Insecure-Requests': '1',
						'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
					}
		self.app_login_url = 'https://m.passport.sohu.com/app/login'
		self.security_login_url = 'https://m.passport.sohu.com/security/login?t={}'
		self.session.headers.update(self.headers)


'''test'''
if __name__ == '__main__':
	sohu().login('', '')