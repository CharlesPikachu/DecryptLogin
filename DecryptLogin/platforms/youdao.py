'''
Function:
	有道模拟登录
		--PC端: http://account.youdao.com/login?service=dict
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
import requests
from hashlib import md5


'''
Function:
	有道模拟登录
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
class youdao():
	def __init__(self, **kwargs):
		self.info = 'youdao'
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
			# 模拟登录
			data = {
					'app': 'web',
					'tp': 'urstoken',
					'cf': '7',
					'fr': '1',
					'ru': 'http://www.youdao.com',
					'product': 'DICT',
					'type': '1',
					'um': 'true',
					'username': username,
					'password': md5(password.encode('utf-8')).hexdigest(),
					'agreePrRule': '1',
					'savelogin': '1'
				}
			res = self.session.post(self.login_url, headers=self.login_headers, data=data, allow_redirects=False)
			# 访问主页
			self.session.get(self.home_url)
			# 获取个人信息
			res = self.session.get(self.accountinfo_url, headers=self.info_headers)
			res_json = res.json()
			# 登录成功
			if res_json['msg'] == 'OK' and res_json['code'] == 0:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 登录失败
			elif res_json['code'] in [2035]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他原因
			else:
				raise RuntimeError(res_json.get('msg'))
		else:
			raise ValueError('Unsupport argument in youdao.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.info_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
								'Host': 'dict.youdao.com',
								'Referer': 'http://dict.youdao.com/wordbook/wordlist?keyfrom=dict2.index'
							}
		self.login_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
								'Host': 'logindict.youdao.com',
								'Origin': 'http://account.youdao.com',
								'Referer': 'http://account.youdao.com/login?service=dict'
							}
		self.home_url = 'http://dict.youdao.com/'
		self.accountinfo_url = 'http://dict.youdao.com/login/acc/query/accountinfo'
		self.login_url = 'https://logindict.youdao.com/login/acc/login'
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	youdao().login('', '')