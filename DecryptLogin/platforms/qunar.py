'''
Function:
	去哪儿旅行模拟登录
		--PC端: http://user.qunar.com/passport/login.jsp
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-04-13
'''
import os
import re
import time
import requests
from ..utils.misc import *


'''
Function:
	去哪儿旅行模拟登录
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
class qunar():
	def __init__(self, **kwargs):
		self.info = 'qunar'
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
			res = self.session.get(self.home_url)
			# 获取验证码
			res = self.session.get(self.captcha_url % str(int(time.time()*1000)))
			saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
			if crackvcFunc is None:
				showImage(os.path.join(self.cur_path, 'captcha.jpg'))
				captcha = input('Input the Verification Code:')
			else:
				captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
			removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
			# 设置cookies
			self.session.get(self.addICK_url)
			res = self.session.get(self.sessionId_url)
			session_id = re.findall(r'sessionId=(.*?)&', res.text)[0]
			self.session.get(self.fid_url % session_id)
			self.session.cookies.update({'QN271': session_id})
			# 模拟登录
			data = {
						'loginType': '0',
						'username': username,
						'password': password,
						'remember': '1',
						'vcode': captcha
					}
			res = self.session.post(self.login_url, data=data)
			res_json = res.json()
			# 登录成功
			if res_json['ret'] and (res_json['errcode'] == 0):
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账号或密码有误
			elif res_json['errcode'] in [21022]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 验证码有误
			elif res_json['errcode'] in [11004]:
				raise RuntimeError('Account -> %s, fail to login, crack captcha error...' % username)
			# 其他原因
			else:
				raise RuntimeError(res_json.get('errmsg'))
		else:
			raise ValueError('Unsupport argument in qunar.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
						}
		self.home_url = 'http://user.qunar.com/passport/login.jsp'
		self.captcha_url = 'https://user.qunar.com/captcha/api/image?k={en7mni(z&p=ucenter_login&c=ef7d278eca6d25aa6aec7272d57f0a9a&t=%s'
		self.addICK_url = 'https://user.qunar.com/passport/addICK.jsp?ssl'
		self.sessionId_url = 'https://rmcsdf.qunar.com/js/df.js?org_id=ucenter.login&js_type=0'
		self.fid_url = 'https://rmcsdf.qunar.com/api/device/challenge.json?sessionId=%s&domain=qunar.com&orgId=ucenter.login'
		self.login_url = 'https://user.qunar.com/passport/loginx.jsp'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	qunar().login('', '')