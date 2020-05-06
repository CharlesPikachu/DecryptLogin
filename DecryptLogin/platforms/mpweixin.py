'''
Function:
	微信公众号模拟登录
		--PC端: https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-05-06
'''
import os
import time
import random
import hashlib
import requests
import warnings
from ..utils.misc import *
warnings.filterwarnings('ignore')


'''
Function:
	微信公众号模拟登录
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
class mpweixin():
	def __init__(self, **kwargs):
		self.info = 'mpweixin'
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
			# 开始登录
			data = {
						'username': username,
						'pwd': hashlib.md5(password.encode('utf-8')).hexdigest(),
						'imgcode': '',
						'f': 'json'
				}
			res = self.session.post(self.startlogin_url, data=data, verify=False)
			res_json = res.json()
			# 请求有误
			if res_json['base_resp']['ret'] != 0:
				# --账户或密码错误
				if res_json['base_resp']['ret'] in [200023]:
					raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
				# --其他
				else:
					raise RuntimeError(res_json['base_resp']['err_msg'])
			# 保障账号安全, 还需要微信扫码
			res = self.session.get(self.getqrcode_url, verify=False)
			saveImage(res.content, os.path.join(self.cur_path, 'qrcode.jpg'))
			showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			# 检测二维码状态
			while True:
				res = self.session.get(self.ask_url, verify=False)
				res_json = res.json()
				# 扫码成功
				if res_json['status'] == 1:
					break
				# 等待扫码/正在扫码
				elif res_json['status'] in [0, 4]:
					pass
				# 其他原因
				else:
					raise RuntimeError(res_json['base_resp']['err_msg'])
				time.sleep(1)
			removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			# 模拟登录
			data = {
					'f': 'json',
					'ajax': '1',
					'random': str(random.random())
				}
			res = self.session.post(self.login_url, data=data, verify=False)
			res_json = res.json()
			# 登录成功
			if res_json['base_resp']['ret'] == 0:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 其他
			else:
				raise RuntimeError(res_json['base_resp']['err_msg'])
		else:
			raise ValueError('Unsupport argument in mpweixin.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
							'Referer': 'https://mp.weixin.qq.com/'
						}
		self.startlogin_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin'
		self.getqrcode_url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300'
		self.ask_url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1'
		self.login_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	mpweixin().login('', '')