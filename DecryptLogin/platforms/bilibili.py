'''
Function:
	B站模拟登录:
		--https://www.bilibili.com/(PC端)
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-15
'''
import rsa
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
			--crackvc_func: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
		Return:
			--infos_return: 用户名等信息
			--session: 登录后的requests.Session()
'''
class bilibili():
	def __init__(self, **kwargs):
		self.info = 'bilibili'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='pc', crackvc_func=None, **kwargs):
		if mode == 'mobile':
			pass
		elif mode == 'pc':
			self.__initializePC()
			# 获得key值
			appkey = '1d8b6e7d45233436'
			data = {
						'appkey': appkey,
						'sign': self.__calcSign(f'appkey={appkey}')
					}
			res = self.session.post(self.getkey_url, data=data)
			res_json = res.json()
			key_hash = res_json['data']['hash']
			pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(res_json['data']['key'].encode())
			# 模拟登录
			data = f"appkey={appkey}&password={urllib.parse.quote_plus(base64.b64encode(rsa.encrypt(f'{key_hash}{password}'.encode(), pub_key)))}&username={urllib.parse.quote_plus(username)}"
			data = f"{data}&sign={self.__calcSign(data)}"
			res = self.session.post(self.login_url, data=data, headers=self.login_headers)
			res_json = res.json()
			# 不需要验证码
			if res_json['code'] == 0 and res_json['data']['status'] == 0:
				for cookie in res_json['data']['cookie_info']['cookies']:
					self.session.cookies.set(cookie['name'], cookie['value'], domain='.bilibili')
			# 需要识别验证码
			elif res_json['code'] == -105:
				captcha_img = self.session.get(self.captcha_url, headers=self.captcha_headers).content
				data = {'image': base64.b64encode(captcha_img).decode('utf-8')}
				captcha = self.session.post(self.crack_captcha_url, json=data).json()['message']
				# --重新获得key值
				appkey = '1d8b6e7d45233436'
				data = {
							'appkey': appkey,
							'sign': self.__calcSign(f'appkey={appkey}')
						}
				res = self.session.post(self.getkey_url, data=data)
				res_json = res.json()
				key_hash = res_json['data']['hash']
				pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(res_json['data']['key'].encode())
				# --重新模拟登录
				data = f"appkey={appkey}&captcha={captcha}&password={urllib.parse.quote_plus(base64.b64encode(rsa.encrypt(f'{key_hash}{password}'.encode(), pub_key)))}&username={urllib.parse.quote_plus(username)}"
				data = f"{data}&sign={self.__calcSign(data)}"
				res = self.session.post(self.login_url, data=data, headers=self.login_headers)
				res_json = res.json()
				# --设置cookie
				if res_json['code'] == 0 and res_json['data']['status'] == 0:
					for cookie in res_json['data']['cookie_info']['cookies']:
						self.session.cookies.set(cookie['name'], cookie['value'], domain='.bilibili')
				else:
					raise RuntimeError('Account -> %s, fail to login, crack captcha error...' % username)
			# 账号密码错误
			elif res_json['code'] == -629:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他错误
			else:
				raise RuntimeError(res_json.get('message'))
			print('[INFO]: Account -> %s, login successfully...' % username)
			infos_return = {'username': username}
			infos_return.update(res_json)
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in Bilibili.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''计算sign值'''
	def __calcSign(self, param):
		salt = "560c52ccd288fed045859ed18bffd973"
		sign_hash = hashlib.md5()
		sign_hash.update(f'{param}{salt}'.encode())
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
		pass


'''test'''
if __name__ == '__main__':
	bilibili().login('', '')