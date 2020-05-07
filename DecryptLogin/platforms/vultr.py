'''
Function:
	Vultr模拟登录:
		--PC端: https://my.vultr.com/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-05
'''
import re
import os
import requests
from hashlib import md5
from ..utils.misc import *


'''
Function:
	Vultr模拟登录
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
class vultr():
	def __init__(self, **kwargs):
		self.info = 'vultr'
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
			res = self.session.get(self.vultr_url)
			# 看看是否需要输入验证码(不支持处理谷歌的点击验证码)
			is_need_verify_code = False
			s = re.findall(r'captcha\.php\?s=(.*?)"', res.text)
			action = re.findall(r'name="action" value="(.*?)"', res.text)[0]
			if s:
				s = s[0]
				is_need_verify_code = True
			if is_need_verify_code:
				res = self.session.get(self.captcha_url.format(s))
				saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
				if crackvcFunc is None:
					showImage(os.path.join(self.cur_path, 'captcha.jpg'))
					captcha = input('Input the captcha:')
				else:
					captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
				removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
			# 模拟登录
			data = {
					'action': action,
					'login_type': 'normal',
					'token': self.__calcToken(action),
					'username': username,
					'password': password
					}
			if is_need_verify_code:
				data['captcha'] = captcha
			res = self.session.post(self.vultr_url, data=data, headers=self.login_headers)
			# 登录失败, 如果网络可以访问谷歌, 很可能是因为出现了谷歌的点击验证码而登录失败, 而非账户/密码/验证码输入错误
			if ('Log In - Vultr.com' in res.text) or 'My Subscriptions - Vultr.com' not in res.text:
				raise RuntimeError('Account -> %s, fail to login, username or password or captcha error. Noted, if your network could visit google.com, maybe you are detected as a robot rather than username or password error...' % username)
			# 登录成功
			name = re.findall(r'Hello, (.*?)!', res.text)[0]
			infos_return = {'username': username, 'name': name}
			print('[INFO]: Account -> %s, login successfully...' % username)
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in vultr.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''计算token'''
	def __calcToken(self, action):
		token = 0
		while True:
			action_hash = md5((action + str(token)).encode(encoding='utf-8')).hexdigest()
			if action_hash[:2] == '00':
				break
			token += 1
		return str(token)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
		self.login_headers = {
								'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
								'referer': 'https://my.vultr.com/',
								'origin': 'https://my.vultr.com',
								'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
								'upgrade-insecure-requests': '1'
							}
		self.vultr_url = 'https://my.vultr.com/'
		self.captcha_url = 'https://my.vultr.com/_images/captcha.php?s={}'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	vultr().login('', '')