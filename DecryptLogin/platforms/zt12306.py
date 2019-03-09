# coding: utf-8
'''
Function:
	12306模拟登录
		--https://www.12306.cn/index/(PC端)
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2019-03-09
'''
import os
import time
import requests
try:
	from .utils.utils import *
except:
	from utils.utils import *


'''
Function:
	12306模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--version: mobile/pc
		Return:
			--session: 登录后的requests.Session()
'''
class zt12306():
	def __init__(self, **kwargs):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
						}
		self.positions = ['36,46', '109,44', '181,47', '254,44', '33,112', '105,116', '186,116', '253,115']
		self.vcode_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5579044251920726'
		self.verify_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
		self.login_url = 'https://kyfw.12306.cn/passport/web/login'
		self.cur_path = os.path.abspath(os.path.dirname(__file__))
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, version='pc'):
		if version == 'mobile':
			return None
		elif version == 'pc':
			self.__downloadVcode()
			time.sleep(0.1)
			res = self.__verifyVcode()
			if not res:
				raise RuntimeError('verification code error...')
			data = {
					'username': username,
					'password': password,
					'appid': 'otn'
					}
			res = self.session.post(self.login_url, headers=self.headers, data=data)
			if res.status_code == 200:
				print('[INFO]: Account -> %s, login successfully...' % username)
				return self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in zt12306.login -> version %s, expect <mobile> or <pc>...' % version)
	'''下载验证码'''
	def __downloadVcode(self):
		res = self.session.get(self.vcode_url, headers=self.headers)
		saveImage(res.content, os.path.join(self.cur_path, 'vcode.jpg'))
		return True
	'''验证码验证'''
	def __verifyVcode(self):
		img_path = os.path.join(self.cur_path, 'vcode.jpg')
		showImage(img_path)
		user_enter = input('Enter the positions of verification code, use <,> to separate, such as <2,3>\n(From left to right, top to bottom -> 1,2,3,4,5,6,7,8):')
		verify_list = []
		for each in user_enter.split(','):
			each = each.strip()
			try:
				verify_list.append(self.positions[int(each)-1])
			except:
				raise RuntimeError('verification code error...')
		data = {
				'answer': ','.join(verify_list),
				'login_site': 'E',
				'rand': 'sjrand'
				}
		res = self.session.post(url=self.verify_url, headers=self.headers, data=data)
		removeImage(img_path)
		if res.json()['result_code'] == '4':
			return True
		else:
			return False


'''test'''
if __name__ == '__main__':
	zt12306().login('', '')