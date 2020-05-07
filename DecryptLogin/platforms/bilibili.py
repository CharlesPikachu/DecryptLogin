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
	2020-05-07
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
	def login(self, username, password, mode='mobile', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			self.__initializeMobile()
			# 是否需要验证码
			is_need_captcha = False
			while True:
				# 需要验证码
				if is_need_captcha:
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
				pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(res_json['data']['key'].encode('utf-8'))
				# 模拟登录
				if is_need_captcha:
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
					is_need_captcha = True
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
			is_need_captcha = False
			while True:
				# 需要验证码
				if is_need_captcha:
					captcha_img = self.session.get(self.captcha_url, headers=self.captcha_headers).content
					data = {'image': base64.b64encode(captcha_img).decode('utf-8')}
					captcha = self.session.post(self.crack_captcha_url, json=data).json()['message']
				# 加密password
				res = self.session.get(self.getkey_url)
				res_json = res.json()
				pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(res_json['key'])
				password = base64.b64encode(rsa.encrypt((res_json['hash'] + password).encode('utf-8'), pubkey))
				# 模拟登录
				data = {
							'appkey': '1d8b6e7d45233436',
							'password': password,
							'username': username
						}
				if is_need_captcha: data.update({'captcha': captcha})
				data_list = list(data.items())
				data_list.sort()
				data_str = urllib.parse.urlencode(data_list)
				sign = self.__calcSign(data_str)
				data['sign'] = sign
				res = self.session.post(self.login_url, data=data)
				res_json = res.json()
				# 不需要验证码, 登录成功
				if res_json['code'] == 0 and res_json['data']['status'] == 0:
					params = {
								'access_key': res_json['data']['token_info']['access_token'],
								'appkey': '1d8b6e7d45233436',
								'gourl': 'https://account.bilibili.com/account/home',
								'ts': str(int(time.time()))
							}
					params_list = list(params.items())
					params_list.sort()
					params_str = urllib.parse.urlencode(params_list)
					sign = self.__calcSign(params_str)
					params['sign'] = sign
					self.session.get(self.login_sso_url, params=params)
					print('[INFO]: Account -> %s, login successfully...' % username)
					infos_return = {'username': username}
					infos_return.update(res_json)
					return infos_return, self.session
				# 需要识别验证码
				elif res_json['code'] == -105:
					is_need_captcha = True
				# 账号密码错误
				elif res_json['code'] == -629:
					raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
				# 其他错误
				else:
					raise RuntimeError(res_json.get('message'))
		else:
			raise ValueError('Unsupport argument in Bilibili.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''计算sign值'''
	def __calcSign(self, param, salt="560c52ccd288fed045859ed18bffd973"):
		sign = hashlib.md5('{}{}'.format(param, salt).encode('utf-8'))
		return sign.hexdigest()
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 BiliDroid/5.51.1 (bbcallen@gmail.com)'
					}
		self.captcha_headers = {
								'Host': 'passport.bilibili.com'
							}
		self.getkey_url = 'http://passport.bilibili.com/login?act=getkey'
		self.login_url = 'https://passport.bilibili.com/api/v3/oauth2/login?'
		self.login_sso_url = 'http://passport.bilibili.com/api/login/sso?'
		self.captcha_url = 'https://passport.bilibili.com/captcha'
		# 破解网站来自: https://github.com/Hsury/Bilibili-Toolkit
		self.crack_captcha_url = 'https://bili.dev:2233/captcha'
		self.session.headers.update({'User-Agent': "Mozilla/5.0 BiliDroid/5.51.1 (bbcallen@gmail.com)"})
	'''初始化移动端'''
	def __initializeMobile(self):
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


'''test'''
if __name__ == '__main__':
	bilibili().login('', '', '')