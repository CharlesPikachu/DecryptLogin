'''
Function:
	小米商城模拟登录
		--PC端: https://www.mi.com/index.html
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
import re
import time
import json
import hashlib
import warnings
import requests
warnings.filterwarnings('ignore')


'''
Function:
	小米商城模拟登录
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
class mieshop():
	def __init__(self, **kwargs):
		self.info = 'mieshop'
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
			# 获得sign等值
			res = self.session.get(self.sign_url, verify=False)
			sign = re.findall(r'"_sign":"(.*?)",', res.text)[0]
			qs = re.findall(r'qs:"(.*?)",', res.text)[0]
			callback = re.findall(r'callback:"(.*?)"', res.text)[0]
			# 模拟登录
			data = {
						'_json': 'true',
						'callback': callback,
						'sid': 'mi_eshop',
						'qs': qs,
						'_sign': sign,
						'serviceParam': '{"checkSafePhone":false}',
						'user': username,
						'hash': hashlib.md5(password.encode(encoding='utf-8')).hexdigest().upper(),
						'cc': '',
						'log': ''
					}
			res = self.session.post(self.login_url % (int(time.time()*1000)), headers=self.login_headers, data=data)
			res_json = json.loads(res.text.replace('&&&START&&&', ''))
			# 登录成功
			if res_json['code'] == 0:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账户密码错误
			elif res_json['code'] in [70016]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他错误
			else:
				raise ValueError(res_json['desc'])
		else:
			raise ValueError('Unsupport argument in mieshop.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
						'Host': 'account.xiaomi.com'
					}
		self.login_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
								'Host': 'account.xiaomi.com',
								'Origin': 'https://account.xiaomi.com',
								'Accept': '*/*',
								'Referer': 'https://account.xiaomi.com/pass/serviceLogin?sid=mi_eshop',
							}
		self.sign_url = 'https://account.xiaomi.com/pass/serviceLogin?sid=mi_eshop'
		self.login_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2?_dc=%s'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	mieshop().login('', '')