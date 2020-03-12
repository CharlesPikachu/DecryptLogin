'''
Function:
	B站模拟登录:
		--PC端: https://www.bilibili.com/
		--移动端: https://passport.bilibili.com/api/v3/oauth2/login
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-29
'''
import rsa
import time
import base64
import urllib
import hashlib
import requests


'''
Function:
	B站模拟登录
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
class bilibili():
	def __init__(self, **kwargs):
		self.info = 'bilibili'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			self.__initializeMobile()
			# 是否需要验证码
			need_verification_code = False
			while True:
				# 需要验证码
				if need_verification_code:
					captcha_img = self.session.get(self.captcha_url, headers=self.captcha_headers).content
					data = {'image': base64.b64encode(captcha_img).decode('utf-8')}
					captcha = self.session.post(self.crack_captcha_url, json=data).json()['message']
				# 获得key值
				app_secret = 'c2ed53a74eeefe3cf99fbd01d8c9c375'
				headers = self.headers.copy()
				headers.update({'ts': str(int(time.time()))})
				headers_sorted = [(k, headers[k]) for k in sorted(headers.keys())]
				sign = urllib.parse.urlencode(headers_sorted)
				sign = hashlib.md5(sign.encode('utf-8') + app_secret.encode('utf-8')).hexdigest()
				data = dict(headers_sorted, **{'sign': sign})
				res = requests.post(self.getkey_url, headers=headers, data=data)
				res_json = res.json()
				key, hash_ = res_json['data']['key'], res_json['data']['hash']
				# 模拟登录
				password = rsa.encrypt((hash_+password).encode(), rsa.PublicKey.load_pkcs1_openssl_pem(key))
				data = {
							'seccode': '',
							'validate': '',
							'subid': '1',
							'permission': 'ALL',
							'username': username,
							'password': base64.b64encode(password),
							'captcha': '',
							'challenge': '',
							'cookies': ''
						}
				if need_verification_code:
					data.update({'captcha': captcha})
				headers = self.headers.copy()
				headers.update({'ts': str(int(time.time()))})
				headers_sorted = dict(data, **headers)
				headers_sorted = [(k, headers_sorted[k]) for k in sorted(headers_sorted.keys())]
				sign = urllib.parse.urlencode(headers_sorted)
				sign = hashlib.md5(sign.encode('utf-8') + app_secret.encode('utf-8')).hexdigest()
				data = dict(headers_sorted, **{'sign': sign})
				res = requests.post(self.login_url, headers=headers, data=data)
				res_json = res.json()
				# 不需要验证码, 登录成功
				if res_json['code'] == 0 and res_json['data']['status'] == 0:
					for cookie in res_json['data']['cookie_info']['cookies']:
						self.session.cookies.set(cookie['name'], cookie['value'], domain='.bilibili')
					print('[INFO]: Account -> %s, login successfully...' % username)
					infos_return = {'username': username}
					infos_return.update(res_json)
					return infos_return, self.session
				# 需要识别验证码
				elif res_json['code'] == -105:
					need_verification_code = True
				# 账号密码错误
				elif res_json['code'] == -629:
					raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
				# 其他错误
				else:
					raise RuntimeError(res_json.get('message'))
		# PC端接口
		elif mode == 'pc':
			self.__initializePC()
			# 是否需要验证码
			need_verification_code = False
			while True:
				# 需要验证码
				if need_verification_code:
					captcha_img = self.session.get(self.captcha_url, headers=self.captcha_headers).content
					data = {'image': base64.b64encode(captcha_img).decode('utf-8')}
					captcha = self.session.post(self.crack_captcha_url, json=data).json()['message']
				# 获得key值
				appkey = '1d8b6e7d45233436'
				data = {
							'appkey': appkey,
							'sign': self.__calcSign('appkey={}'.format(appkey))
						}
				res = self.session.post(self.getkey_url, data=data)
				res_json = res.json()
				key_hash = res_json['data']['hash']
				pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(res_json['data']['key'].encode())
				# 模拟登录
				if need_verification_code:
					data = "appkey={}&captcha={}&password={}&username={}".format(appkey, captcha, urllib.parse.quote_plus(base64.b64encode(rsa.encrypt('{}{}'.format(key_hash, password).encode(), pub_key))), urllib.parse.quote_plus(username))
				else:
					data = "appkey={}&password={}&username={}".format(appkey, urllib.parse.quote_plus(base64.b64encode(rsa.encrypt('{}{}'.format(key_hash, password).encode(), pub_key))), urllib.parse.quote_plus(username))
				data = "{}&sign={}".format(data, self.__calcSign(data))
				res = self.session.post(self.login_url, data=data, headers=self.login_headers)
				res_json = res.json()
				# 不需要验证码, 登录成功
				if res_json['code'] == 0 and res_json['data']['status'] == 0:
					for cookie in res_json['data']['cookie_info']['cookies']:
						self.session.cookies.set(cookie['name'], cookie['value'], domain='.bilibili')
					print('[INFO]: Account -> %s, login successfully...' % username)
					infos_return = {'username': username}
					infos_return.update(res_json)
					return infos_return, self.session
				# 需要识别验证码
				elif res_json['code'] == -105:
					need_verification_code = True
				# 账号密码错误
				elif res_json['code'] == -629:
					raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
				# 其他错误
				else:
					raise RuntimeError(res_json.get('message'))
		else:
			raise ValueError('Unsupport argument in Bilibili.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''计算sign值'''
	def __calcSign(self, param):
		salt = "560c52ccd288fed045859ed18bffd973"
		sign_hash = hashlib.md5()
		sign_hash.update('{}{}'.format(param, salt).encode())
		return sign_hash.hexdigest()
	'''初始化PC端'''
	def __initializePC(self):
		self.login_headers = {
								'Content-type': 'application/x-www-form-urlencoded'
							}
		self.captcha_headers = {
								'Host': 'passport.bilibili.com'
							}
		self.getkey_url = 'https://passport.bilibili.com/api/oauth2/getKey'
		self.login_url = 'https://passport.bilibili.com/api/v2/oauth2/login'
		self.captcha_url = 'https://passport.bilibili.com/captcha'
		# 破解网站来自: https://github.com/Hsury/Bilibili-Toolkit
		self.crack_captcha_url = 'https://bili.dev:2233/captcha'
		self.session.headers.update({'User-Agent': "Mozilla/5.0 BiliDroid/5.51.1 (bbcallen@gmail.com)"})
	'''初始化移动端'''
	def __initializeMobile(self):
		self.headers = {
						'access_key': '',
						'actionKey': 'appkey',
						'appkey': '27eb53fc9058f8c3',
						'build': '8400',
						'device': 'phone',
						'mobi_app': 'iphone',
						'platform': 'ios',
						'ts': '',
						'type': 'json'
					}
		self.captcha_headers = {
								'Host': 'passport.bilibili.com'
							}
		self.getkey_url = 'https://passport.bilibili.com/api/oauth2/getKey'
		self.login_url = 'https://passport.bilibili.com/api/v3/oauth2/login'
		self.captcha_url = 'https://passport.bilibili.com/captcha'
		# 破解网站来自: https://github.com/Hsury/Bilibili-Toolkit
		self.crack_captcha_url = 'https://bili.dev:2233/captcha'


'''test'''
if __name__ == '__main__':
	bilibili().login('', '', '')