'''
Function:
	微博模拟登录:
		--https://login.sina.com.cn/signup/signin.php(PC端)
		--https://m.weibo.cn/(移动端)
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2019-12-09
'''
import re
import rsa
import time
import random
import base64
import requests
import warnings
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
			--version: mobile/pc
		Return:
			--session: 登录后的requests.Session()
'''
class weibo():
	def __init__(self, **kwargs):
		self.info = 'weibo'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, version='mobile'):
		if version == 'mobile':
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
			if res.json()['retcode'] == 20000000:
				print('[INFO]: Account -> %s, login successfully...' % username)
				return username, self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		elif version == 'pc':
			self.__initializePC()
			# 请求prelogin_url
			su = base64.b64encode(username.encode())
			params = {
						'entry': 'weibo',
						'callback': 'sinaSSOController.preloginCallBack',
						'su': su,
						'rsakt': 'mod',
						'checkpin': '1',
						'client': 'ssologin.js(v1.4.19)',
						'_': str(int(time.time()*1000))
					}
			res = self.session.get(self.prelogin_url, headers=self.headers, params=params, verify=False)
			nonce = re.findall(r'"nonce":"(.*?)"', res.text)[0]
			pubkey = re.findall(r'"pubkey":"(.*?)"', res.text)[0]
			rsakv = re.findall(r'"rsakv":"(.*?)"', res.text)[0]
			servertime = re.findall(r'"servertime":(.*?),', res.text)[0]
			# 请求ssologin_url
			publickey = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
			sp = rsa.encrypt((str(servertime)+'\t'+nonce+'\n'+password).encode(), publickey)
			sp = b2a_hex(sp)
			data_post = {
							'entry': 'weibo',
							'gateway': '1',
							'from': '',
							'savestate': '7',
							'qrcode_flag': 'false',
							'useticket': '1',
							'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
							'vsnf': '1',
							'su': su,
							'service': 'miniblog',
							'servertime': str(int(servertime)+random.randint(1, 20)),
							'nonce': nonce,
							'pwencode': 'rsa2',
							'rsakv': rsakv,
							'sp': sp,
							'sr': '1536 * 864',
							'encoding': 'UTF - 8',
							'prelt': '35',
							'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
							'returntype': 'META'
						}
			res = self.session.post(self.ssologin_url, headers=self.headers, data=data_post, allow_redirects=False, verify=False)
			redirect_url = re.findall(r'location.replace\("(.*?)"\);', res.text)[0]
			res = self.session.get(redirect_url, headers=self.headers, allow_redirects=False, verify=False)
			ticket, ssosavestate = re.findall(r'ticket=(.*?)&ssosavestate=(.*?)"', res.text)[0]
			# 请求login_url
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
				return username, self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in weibo.login -> version %s, expect <mobile> or <pc>...' % version)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
						}
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