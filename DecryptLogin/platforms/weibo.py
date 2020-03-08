'''
Function:
	微博模拟登录:
		--PC端: https://login.sina.com.cn/signup/signin.php
		--移动端: https://m.weibo.cn/
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-29
'''
import re
import rsa
import time
import random
import base64
import requests
import warnings
from ..utils.misc import *
from binascii import b2a_hex
warnings.filterwarnings('ignore')


'''
Function:
	微博模拟登录
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
class weibo():
	def __init__(self, **kwargs):
		self.info = 'weibo'
		self.cur_path = os.getcwd()
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='mobile', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			self.__initializeMobile()
			data = {
					'username': username,
					'password': password,
					'savestate': '1',
					'r': 'https://weibo.cn/',
					'ec': '0',
					'pagerefer': 'https://weibo.cn/pub/',
					'entry': 'mweibo',
					'wentry': '',
					'loginfrom': '',
					'client_id': '',
					'code': '',
					'qq': '',
					'mainpageflag': '1',
					'hff': '',
					'hfp': ''
					}
			res = self.session.post(self.login_url, headers=self.login_headers, data=data)
			res_json = res.json()
			# 登录成功
			if res_json['retcode'] == 20000000:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 用户名或密码错误
			elif res_json['retcode'] == 50011002:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他错误
			else:
				raise RuntimeError(res_json['msg'])
		# PC端接口
		elif mode == 'pc':
			self.__initializePC()
			# 进行模拟登录
			add_verification_code = False
			while True:
				# --是否需要验证码
				if add_verification_code:
					params = {
								'r': str(int(random.random()*100000000)),
								's': '0'
							}
					res = self.session.get(self.pin_url, headers=self.headers, params=params)
					saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
					if crackvcFunc is None:
						showImage(os.path.join(self.cur_path, 'captcha.jpg'))
						captcha = input('Input the Verification Code:')
					else:
						captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
					removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
				# --请求prelogin_url
				su = base64.b64encode(username.encode())
				params = {
							'entry': 'weibo',
							'su': su,
							'rsakt': 'mod',
							'checkpin': '1',
							'client': 'ssologin.js(v1.4.19)',
							'_': str(int(time.time()*1000))
						}
				res = self.session.get(self.prelogin_url, headers=self.headers, params=params, verify=False)
				res_json = res.json()
				nonce = res_json.get('nonce', '')
				pubkey = res_json.get('pubkey', '')
				rsakv = res_json.get('rsakv', '')
				servertime = res_json.get('servertime', '')
				# --请求ssologin_url
				publickey = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
				sp = rsa.encrypt((str(servertime)+'\t'+nonce+'\n'+password).encode(), publickey)
				sp = b2a_hex(sp)
				data_post = {
								'entry': 'account',
								'gateway': '1',
								'from': '',
								'savestate': '30',
								'useticket': '0',
								'useticket': '1',
								'pagerefer': '',
								'vsnf': '1',
								'su': su,
								'service': 'account',
								'servertime': str(int(servertime)+random.randint(1, 20)),
								'nonce': nonce,
								'pwencode': 'rsa2',
								'rsakv': rsakv,
								'sp': sp,
								'sr': '1536 * 864',
								'encoding': 'UTF - 8',
								'cdult': '3',
								'domain': 'sina.com.cn',
								'prelt': '95',
								'returntype': 'TEXT'
							}
				if add_verification_code:
					data_post['door'] = captcha
				res = self.session.post(self.ssologin_url, headers=self.headers, data=data_post, allow_redirects=False, verify=False)
				res_json = res.json()
				# --登录成功
				if res_json['retcode'] == '0':
					break
				# --用户名或密码错误
				elif res_json['retcode'] == '101':
					raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
				# --验证码错误
				elif res_json['retcode'] == '2070':
					raise RuntimeError('Account -> %s, fail to login, crack captcha error...' % username)
				# --需要验证码
				elif res_json['retcode'] == '4049':
					add_verification_code = True
				# --其他错误
				else:
					raise RuntimeError(res_json.get('reason', ''))
			ticket, ssosavestate = re.findall(r'ticket=(.*?)&ssosavestate=(.*?)"', res.text)[0]
			# 请求login_url和home_url, 进一步验证登录是否成功
			params = {
						'ticket': ticket,
						'ssosavestate': str(ssosavestate),
						'callback': 'sinaSSOController.doCrossDomainCallBack',
						'scriptId': 'ssoscript0',
						'client': 'ssologin.js(v1.4.19)',
						'_': str(int(time.time() * 1000))
					}
			params = '&'.join(['%s=%s' % (key, value) for key, value in params.items()])
			res = self.session.get(self.login_url+params, headers=self.headers, verify=False)
			uid = re.findall(r'"uniqueid":"(.*?)"', res.text)[0]
			res = self.session.get(self.home_url % uid, headers=self.headers, verify=False)
			if '我的首页' in res.text:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, visit %s error...' % (username, self.home_url % uid))
		else:
			raise ValueError('Unsupport argument in weibo.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
						}
		self.pin_url = 'https://login.sina.com.cn/cgi/pin.php'
		self.prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php?'
		self.ssologin_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
		self.login_url = 'https://passport.weibo.com/wbsso/login?'
		self.home_url = 'https://weibo.com/u/%s/home'
	'''初始化移动端'''
	def __initializeMobile(self):
		self.login_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
								'Accept': '*/*',
								'Accept-Encoding': 'gzip, deflate, br',
								'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
								'Connection': 'keep-alive',
								'Origin': 'https://passport.weibo.cn',
								'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
							}
		self.login_url = 'https://passport.weibo.cn/sso/login'


'''test'''
if __name__ == '__main__':
	weibo().login('', '', '')