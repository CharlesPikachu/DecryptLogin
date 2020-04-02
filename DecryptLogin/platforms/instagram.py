'''
Function:
	Instagram模拟登录
		--PC端: https://www.instagram.com/
		--移动端暂不支持
Author:
	Leon Wee
GitHub:
	https://github.com/leon-sleepinglion
更新日期:
	2020-04-01
'''
import re
import requests


'''
Function:
	Instagram模拟登录
Detail:
	-login:
		Input:
			--username: 用户名/邮箱/手机号
			--password: 密码
			--mode: mobile/pc
			--crackvcFunc: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
			--proxies: 为requests.Session()设置代理
		Return:
			--infos_return: 用户名等信息
			--session: 登录后的requests.Session()
'''
class instagram():
	def __init__(self, **kwargs):
		self.info = 'instagram'
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
			self.login_headers['x-csrftoken'] = self.__getToken()
			data = {
					'username': username,
					'password': password,
					'optIntoOneTap': False,
					}
			res = self.session.post(self.login_url, headers=self.login_headers, data=data)
			if res.status_code == 200 and '"authenticated": true' in res.text:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				return infos_return, self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in instagram.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''获取csrf_token参数'''
	def __getToken(self):
		res = self.session.get(self.main_url)
		token = re.findall(r'csrf_token":"\w+', res.text)[0].split(':"')[1]
		return token
	'''初始化PC端'''
	def __initializePC(self):
		self.login_headers = {
								'scheme': 'https',
								'accept': '*/*',
								'accept-encoding': 'gzip, deflate, br',
								'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,ms;q=0.5,zh-TW;q=0.4,id;q=0.3',
								'content-length': '300',
								'content-type': 'application/x-www-form-urlencoded',
								'origin': 'https://www.instagram.com',
								'referer': 'https://www.instagram.com/',
								'sec-fetch-dest': 'empty',
								'sec-fetch-mode': 'cors',
								'sec-fetch-site': 'same-origin',
								'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
								'x-csrftoken': '',
								'x-requested-with': 'XMLHttpRequest'
							}
		self.main_url = 'https://www.instagram.com/'
		self.login_url = self.main_url + 'accounts/login/ajax/'
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	instagram().login('', '')