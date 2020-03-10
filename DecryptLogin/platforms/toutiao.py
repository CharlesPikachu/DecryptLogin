'''
Function:
	今日头条模拟登录:
		--PC端暂不支持
		--移动端: https://m.toutiao.com/
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
import re
import base64
import requests
from ..utils.misc import *


'''
Function:
	今日头条模拟登录
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
class toutiao():
	def __init__(self, **kwargs):
		self.info = 'toutiao'
		self.cur_path = os.getcwd()
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='mobile', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			self.__initializeMobile()
			# 先访问头条主页
			self.session.get(url=self.home_url, headers=self.headers)
			# 无验证码登录尝试
			data = {
						'account': username,
						'password': password,
						'captcha': '',
						'is_30_days_no_login': 'true',
						'service': 'https://www.toutiao.com/'
					}
			res = self.session.post(url=self.login_url, data=data, headers=self.headers)
			res_json = res.json()
			# 登录成功
			if res_json.get('error_code') == 0:
				redirect_url = res_json.get('redirect_url')
				self.session.get(redirect_url, timeout=3)
				ticket = re.findall("ticket=(.*)", redirect_url)[0]
			# 需要输入验证码
			elif res_json.get('error_code') in [1101, 1102] and res_json.get('captcha'):
				image = base64.b64decode(res_json.get('captcha'))
				saveImage(image, os.path.join(self.cur_path, 'captcha.jpg'))
				if crackvcFunc is None:
					showImage(os.path.join(self.cur_path, 'captcha.jpg'))
					captcha = input('Input the Verification Code:')
				else:
					captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
				data['captcha'] = captcha
				res = self.session.post(url=self.login_url, data=data, headers=self.headers)
				res_json = res.json()
				if res_json.get('error_code') == 0:
					redirect_url = res_json.get('redirect_url')
					self.session.get(redirect_url, timeout=3)
					ticket = re.findall("ticket=(.*)", redirect_url)[0]
				else:
					raise RuntimeError('Account -> %s, fail to login, crack captcha error...' % username)
			# 账号密码错误
			elif res_json.get('error_code') in [1009, 1003]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他问题
			else:
				raise RuntimeError(res_json.get('description'))
			print('[INFO]: Account -> %s, login successfully...' % username)
			infos_return = {'username': username, 'userid': res_json.get('user_id'), 'ticket': ticket}
			return infos_return, self.session
		# PC端接口
		elif mode == 'pc':
			raise NotImplementedError
		else:
			raise ValueError('Unsupport argument in toutiao.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		pass
	'''初始化移动端'''
	def __initializeMobile(self):
		self.headers = {
							'Host': 'sso.toutiao.com',
							'Origin': 'https://sso.toutiao.com',
							'Referer': 'https://m.toutiao.com/',
							'Upgrade-Insecure-Requests': '1',
							'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
						}
		self.home_url = 'https://m.toutiao.com/'
		self.login_url = 'https://sso.toutiao.com/account_login/'


'''test'''
if __name__ == '__main__':
	toutiao().login('', '')