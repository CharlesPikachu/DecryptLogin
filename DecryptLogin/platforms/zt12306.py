'''
Function:
	12306模拟登录
		--PC端: https://www.12306.cn/index/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-05-07
'''
import os
import time
import requests
from ..utils.misc import *


'''
Function:
	12306模拟登录
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
class zt12306():
	def __init__(self, **kwargs):
		self.info = 'zt12306'
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
			self.__downloadCaptcha()
			time.sleep(0.1)
			res = self.__verifyCaptcha(crackvcFunc)
			if not res:
				raise RuntimeError('Account -> %s, fail to login, crack captcha error...' % username)
			data = {
					'username': username,
					'password': password,
					'appid': 'otn'
					}
			res = self.session.post(self.login_url, headers=self.headers, data=data)
			if res.status_code == 200:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				return infos_return, self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in zt12306.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''下载验证码'''
	def __downloadCaptcha(self):
		res = self.session.get(self.captcha_url, headers=self.headers)
		saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
		return True
	'''验证码验证'''
	def __verifyCaptcha(self, crackvcFunc):
		img_path = os.path.join(self.cur_path, 'captcha.jpg')
		if crackvcFunc is None:
			showImage(img_path)
			user_enter = input('Enter the positions of captcha, use <,> to separate, such as <2,3>\n(From left to right, top to bottom -> 1,2,3,4,5,6,7,8):')
		else:
			user_enter = crackvcFunc(img_path)
		digital_list = []
		for each in user_enter.split(','):
			each = each.strip()
			try:
				digital_list.append(self.positions[int(each)-1])
			except:
				raise RuntimeError('captcha format error...')
		data = {
				'answer': ','.join(digital_list),
				'login_site': 'E',
				'rand': 'sjrand'
				}
		res = self.session.post(url=self.captcha_check_url, headers=self.headers, data=data)
		removeImage(img_path)
		if res.json()['result_code'] == '4':
			return True
		else:
			return False
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
						}
		self.positions = ['36,46', '109,44', '181,47', '254,44', '33,112', '105,116', '186,116', '253,115']
		self.captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5579044251920726'
		self.captcha_check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
		self.login_url = 'https://kyfw.12306.cn/passport/web/login'
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	zt12306().login('', '')