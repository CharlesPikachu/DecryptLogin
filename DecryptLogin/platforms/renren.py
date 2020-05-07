'''
Function:
	人人网模拟登录
		--PC端: http://www.renren.com/PLogin.do
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-07
'''
import os
import re
import random
import requests
from ..utils.misc import *


'''
Function:
	人人网模拟登录
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
class renren():
	def __init__(self, **kwargs):
		self.info = 'renren'
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
			# 判断是否需要验证码
			is_need_captcha = False
			res = self.session.get(self.home_url)
			if 'id="verifyPic_login"' in res.text:
				is_need_captcha = True
			# 如果需要验证码, 则获取验证码
			if is_need_captcha:
				res = self.session.get(self.captcha_url.format(random.random()))
				saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
				if crackvcFunc is None:
					showImage(os.path.join(self.cur_path, 'captcha.jpg'))
					captcha = input('Input the captcha:')
				else:
					captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
				removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
			# 进行登录
			data = {
						'email': username,
						'origURL': 'http://www.renren.com/home',
						'domain': 'renren.com',
						'key_id': 1,
						'captcha_type': 'web_login',
						'password': password,
						'f': ''
					}
			if is_need_captcha: data.update({'icode': captcha})
			res = self.session.post(self.login_url, data=data)
			user_id = re.findall(r'id:"(.*?)",', res.text.replace('\n', '').replace(' ', ''))
			user_ruid = re.findall(r'ruid:"(.*?)",', res.text.replace('\n', '').replace(' ', ''))
			name = re.findall(r'name:"(.*?)",', res.text.replace('\n', '').replace(' ', ''))
			privacy = re.findall(r'privacy:"(.*?)",', res.text.replace('\n', '').replace(' ', ''))
			request_token = re.findall(r"requestToken:'(.*?)',", res.text.replace('\n', '').replace(' ', ''))
			_rtk = re.findall(r"_rtk:'(.*?)'}", res.text.replace('\n', '').replace(' ', ''))
			is_vip = re.findall(r'user.isvip=(.*?);', res.text.replace('\n', '').replace(' ', ''))
			# 登录失败(一般就是账户或密码错误)
			if (not name[0]) and (u'不匹配' in res.text):
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 登录成功
			print('[INFO]: Account -> %s, login successfully...' % username)
			infos_return = {'username': username, 'id': user_id[0], 
							'ruid': user_ruid[0], 'name': name[0], 
							'privacy': privacy[0], 'requestToken': request_token[0],
							'_rtk': _rtk[0], 'isvip': is_vip[0]}
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in renren.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
					}
		self.home_url = 'http://renren.com/'
		self.login_url = 'http://www.renren.com/PLogin.do'
		self.captcha_url = 'http://icode.renren.com/getcode.do?t=web_login&rnd={}'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	renren().login('', '')