'''
Function:
	中关村在线模拟登录:
		--PC端: http://www.zol.com.cn/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-29
'''
import time
import requests
from hashlib import md5


'''
Function:
	中关村在线模拟登录
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
class zgconline():
	def __init__(self, **kwargs):
		self.info = 'zgconline'
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
			# 请求home_url
			self.session.get(self.home_url)
			# 请求login_url
			data = {
						'userid': username,
						'pwd': md5((password+'zol').encode(encoding='utf-8')).hexdigest(),
						'is_auto': '1',
						'backUrl': 'http://www.zol.com.cn/'
					}
			cookies = {'ip_ck': self.__getIPCK()}
			self.session.headers.update({'Content-type': 'application/x-www-form-urlencoded'})
			res = self.session.post(self.login_url, data=data, cookies=cookies)
			res_json = res.json()
			# 登录成功
			if res_json.get('info') == 'ok':
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账号或密码有误
			elif res_json.get('info') == 'error' and res_json.get('msg') == '账号或密码错误,请重试':
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他原因
			else:
				raise RuntimeError(res_json.get('msg'))
		else:
			raise ValueError('Unsupport argument in zgconline.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''获得ipck'''
	def __getIPCK(self):
		res = self.session.get(self.ipck_url.format(int(time.time()/1000), ''))
		return res.json().get('ipck')
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
							'Referer': 'http://service.zol.com.cn/user/login.php?backUrl=http://www.zol.com.cn/',
							'Origin': 'http://service.zol.com.cn'
						}
		self.home_url = 'http://www.zol.com.cn/'
		self.login_url = 'http://service.zol.com.cn/user/ajax/login2014/login.php'
		self.ipck_url = 'http://js.zol.com.cn/pvn/pv.ht?&t={}&c={}'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	zgconline().login('', '')