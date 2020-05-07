'''
Function:
	百度网盘模拟登录
		--PC端: https://wappass.baidu.com/wp/api/login
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-10
'''
import os
import re
import rsa
import time
import json
import requests
from ..utils.misc import *


'''
Function:
	百度网盘模拟登录
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
class baidupan():
	def __init__(self, **kwargs):
		self.info = 'baidupan'
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
			# 访问home_url, 初始化cookies
			self.session.get(self.home_url)
			# 获得servertime
			servertime = self.__getServertime()
			# 获得publickkey
			publickkey_modulus, publickkey_exponent = self.__getPublicKey()
			# 获得traceid
			traceid = self.__getTraceId()
			# 加密password
			password = self.__unpaddingRSA(publickkey_modulus, publickkey_exponent, str(password)+str(servertime))
			# 获得时间戳
			timestamp = str(int(time.time()/1000)) + '773_357'
			# 模拟登录
			is_need_captcha = False
			is_need_phone_email_verify = False
			captcha = ''
			codestring = ''
			goto_url = ''
			while True:
				# --需要图片验证码
				if is_need_captcha:
					res = self.session.get(self.genimage_url+codestring)
					saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
					if crackvcFunc is None:
						showImage(os.path.join(self.cur_path, 'captcha.jpg'))
						captcha = input('Input the captcha:')
					else:
						captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
					removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
				# --需要验证手机/邮箱
				if is_need_phone_email_verify:
					res_json = self.__verifyPhoneEmail(goto_url)
					self.session.get(res_json['data']['u'])
				# --不需要验证手机/邮箱, 直接构造并发送登录请求
				if not is_need_phone_email_verify:
					data = {
							'username': username,
							'password': password,
							'verifycode': captcha,
							'vcodestr': codestring,
							'isphone': '0',
							'loginmerge': '1',
							'action': 'login',
							'uid': timestamp,
							'skin': 'default_v2',
							'connect': '0',
							'dv': 'tk0.0095975573224773571583831604201@aadbAkqLI24oCwthDIxGB4p0K-2RKwxRuKp-sZxYJmRY9V2ZGq__rd0tmpV6wAk2zomRZ9DBLI24oCwthDIxGB4p0K-2RKwx-sntgOKCTp-9YAk2Y9SR~9-6QA4ChD1sH0BwGKwhDB4T~94xGMv4-MQsiM3CTCmmOEmuldwJ5hudj9HRYAkFRBdbsvLRAVqRoDBWp-Bwp-9Y9V0Qp-9wp-2wok9z9-2Z9k0Y9k2_jdVOrClMr9cAYxQsQMju348JrBjuZxgAY~wP3CXJ3XjJn0_~db9mRRAk2w9D1L9VFlAk2w9-uLokulAk2w9-uL9DB-pSRz9V0_',
							'getpassUrl': '/passport/getpass?clientfrom=&adapter=0&ssid=&from=&authsite=&bd_page_type=&uid="+timestamp+"&pu=&tpl=wimn&u=https://m.baidu.com/usrprofile%3Fuid%3D"+timestamp+"%23logined&type=&bdcm=060d5ffd462309f7e5529822720e0cf3d7cad665&tn=&regist_mode=&login_share_strategy=&subpro=wimn&skin=default_v2&client=&connect=0&smsLoginLink=1&loginLink=&bindToSmsLogin=&overseas=&is_voice_sms=&subpro=wimn&hideSLogin=&forcesetpwd=&regdomestic=',
							'mobilenum': 'undefined',
							'servertime': servertime,
							'gid': 'DA7C3AE-AF1F-48C0-AF9C-F1882CA37CD5',
							'logLoginType': 'wap_loginTouch',
							'FP_UID': '0b58c206c9faa8349576163341ef1321',
							'traceid': traceid
						}
					res = self.session.post(self.login_url, headers=self.login_headers, data=data)
					res_json = res.json()
				# --登录成功
				if res_json['errInfo'].get('no') in ['0']:
					print('[INFO]: Account -> %s, login successfully...' % username)
					infos_return = {'username': username}
					infos_return.update(res_json)
					return infos_return, self.session
				# --需要验证码
				elif res_json['errInfo'].get('no') in ['500002']:
					codestring = res_json['data'].get('codeString')
					is_need_captcha = True
				# --需要验证手机/邮箱
				elif res_json['errInfo'].get('no') in ['400101', '400023']:
					goto_url = res_json.get('data').get('gotoUrl')
					is_need_phone_email_verify = True
					is_need_captcha = False
				# --账户或密码错误
				elif res_json['errInfo'].get('no') in ['400010']:
					raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
				# --其他原因
				else:
					raise RuntimeError(res_json['errInfo'].get('msg'))
		else:
			raise ValueError('Unsupport argument in baidupan.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''手机/邮箱验证'''
	def __verifyPhoneEmail(self, goto_url):
		# 提取必要的数据
		res = self.session.get(goto_url)
		res.encoding = 'utf-8'
		raw_phone = re.search(r'<p class="verify-type-li-tiptop">(.*?)</p>\s+<p class="verify-type-li-tipbottom">通过手机验证码验证身份</p>', res.text)
		raw_email = re.search(r'<p class="verify-type-li-tiptop">(.*?)</p>\s+<p class="verify-type-li-tipbottom">通过邮箱验证码验证身份</p>', res.text)
		raw_token = re.search(r'token=([^&]+).*?&u=([^&]+)&', goto_url)
		phone = raw_phone.group(1) if raw_phone else None
		email = raw_phone.group(1) if raw_email else None
		token, u = raw_token.group(1), raw_token.group(2)
		# 选择验证方式
		verify_type = input('Your account has to be verified by using binded phone or email, please choose phone(enter 0, by default) or email(enter 1):')
		verify_type = 'email' if verify_type == '1' else 'mobile'
		# 发送验证码
		url = 'https://wappass.baidu.com/passport/authwidget?action=send&tpl=&type={}&token={}&from=&skin=&clientfrom=&adapter=2&updatessn=&bindToSmsLogin=&upsms=&finance='.format(verify_type, token)
		res = self.session.get(url)
		# 输入验证码
		vcode = input('Please enter the verify code you have accepted:')
		# 验证验证码
		headers = {
					'Connection': 'keep-alive',
					'Host': 'wappass.baidu.com',
					'Upgrade-Insecure-Requests': '1',
					'Pragma': 'no-cache'
				}
		timestamp = str(int(time.time())) + '773_357994'
		url = 'https://wappass.baidu.com/passport/authwidget?v={}&vcode={}&token={}&u={}&action=check&type={}&tpl=&skin=&clientfrom=&adapter=2&updatessn=&bindToSmsLogin=&isnew=&card_no=&finance=&callback=jsonp1'.format(timestamp, vcode, token, u, verify_type)
		res = self.session.get(url, headers=headers)
		res_json = res.text[len("jsonp1("): -1].strip()
		res_json = json.loads(res_json)
		return res_json
	'''unpadding RSA'''
	def __unpaddingRSA(self, publickkey_modulus, publickkey_exponent, message):
		def padMSG(message, target_length):
			message = message[::-1]
			max_msglength = target_length - 11
			msglength = len(message)
			padding = b''
			padding_length = target_length - msglength - 3
			for i in range(padding_length):
				padding += b'\x00'
			return b''.join([b'\x00\x00', padding, b'\x00', message])
		def encrypt(message, pubkey):
			keylength = rsa.common.byte_size(pubkey.n)
			padded = padMSG(message, keylength)
			payload = rsa.transform.bytes2int(padded)
			encrypted = rsa.core.encrypt_int(payload, pubkey.e, pubkey.n)
			block = rsa.transform.int2bytes(encrypted, keylength)
			return block
		m = int(publickkey_modulus, 16)
		e = int(publickkey_exponent, 16)
		rsa_pubkey = rsa.PublicKey(m, e)
		crypto = encrypt(message.encode('utf-8'), rsa_pubkey)
		return crypto.hex()
	'''获得servertime'''
	def __getServertime(self):
		res = self.session.get(self.servertime_url)
		servertime = res.json().get('time')
		return servertime
	'''获得publickey'''
	def __getPublicKey(self):
		res = self.session.get(self.publickkey_url)
		publickkey_modulus = re.findall(r',rsa:\"(.*?)\",error:', res.text)
		publickkey_modulus = publickkey_modulus[0] if len(publickkey_modulus) > 0 else "B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F"
		publickkey_exponent = '10001'
		return publickkey_modulus, publickkey_exponent
	'''获得traceid'''
	def __getTraceId(self):
		res = self.session.get(self.traceid_url)
		traceid = res.headers.get('Trace-Id')
		return traceid
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
						'Referer': 'https://www.baidu.com/'
						}
		self.login_headers = {
								'Content-Type': 'application/x-www-form-urlencoded',
								'Accept': 'application/json',
								'Referer': 'https://wappass.baidu.com/',
								'X-Requested-With': 'XMLHttpRequest',
								'Connection': 'keep-alive'
							}
		self.home_url = 'https://www.baidu.com/'
		self.servertime_url = 'https://wappass.baidu.com/wp/api/security/antireplaytoken'
		self.publickkey_url = 'https://wappass.baidu.com/static/touch/js/login_d9bffc9.js'
		self.traceid_url = 'https://wappass.baidu.com/'
		self.login_url = 'https://wappass.baidu.com/wp/api/login'
		self.genimage_url = 'https://wappass.baidu.com/cgi-bin/genimage?'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	baidupan().login('', '')