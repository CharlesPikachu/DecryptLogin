'''
Function:
	凤凰网模拟登录:
		--PC端: https://id.ifeng.com/user/login
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-29
'''
import os
import requests
from ..utils.misc import *


'''
Function:
	凤凰网模拟登录
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
class ifeng():
	def __init__(self, **kwargs):
		self.info = 'ifeng'
		self.cur_path = os.getcwd()
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
			# 访问登录主页user_login_url
			self.session.get(self.user_login_url)
			# 获取验证码
			res = self.session.get(self.authcode_url)
			saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
			if crackvcFunc is None:
				showImage(os.path.join(self.cur_path, 'captcha.jpg'))
				captcha = input('Input the captcha:')
			else:
				captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
			removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
			# 请求登录接口api_login_url进行模拟登录
			self.session.headers.update({
											'Upgrade-Insecure-Requests': '1',
											'Content-Type': 'application/x-www-form-urlencoded',
											'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
											'Referer': 'http://id.ifeng.com/allsite/login'
										})
			data = {
						'u': username,
						'k': password,
						'auth': captcha,
						'type': '3',
						'confrom': ''
					}
			res = self.session.post(self.api_login_url, data=data)
			res_json = res.json()
			# 登录成功
			if res_json.get('code') == 1 and res_json.get('msgcode') == '0':
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 验证码错误
			elif res_json.get('code') == 0 and res_json.get('msgcode') == '4009':
				raise RuntimeError('Account -> %s, fail to login, crack captcha error...' % username)
			# 用户名或密码错误
			elif res_json.get('code') == 0 and res_json.get('msgcode') == '8003':
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他错误
			else:
				raise RuntimeError(res_json.get('message'))
		else:
			raise ValueError('Unsupport argument in ifeng.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'Host': 'id.ifeng.com',
						'Origin': 'https://id.ifeng.com',
						'Referer': 'https://id.ifeng.com/user/login',
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
					}
		self.user_login_url = 'https://id.ifeng.com/user/login'
		self.api_login_url = 'https://id.ifeng.com/api/login'
		self.authcode_url = 'https://id.ifeng.com/public/authcode'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	ifeng().login('', '')