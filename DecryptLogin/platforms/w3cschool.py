'''
Function:
	w3cshool模拟登录
		--PC端: https://www.w3cschool.cn/login?refer=/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-08
'''
import requests


'''
Function:
	w3cshool模拟登录
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
class w3cschool():
	def __init__(self, **kwargs):
		self.info = 'w3cschool'
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
			# 访问一下登录页面
			self.session.get(self.home_url)
			# 模拟登录
			data = {
					'fromid': '',
					'username': username,
					'password': password,
					'remember': '1',
					'scode': ''
				}
			res = self.session.post(self.login_url, data=data)
			res_json = res.json()
			# 登录成功
			if res_json['statusCode'] == 200:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账号或密码错误
			elif res_json['statusCode'] in [301]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他错误
			else:
				raise RuntimeError(res_json.get('message'))
		else:
			raise ValueError('Unsupport argument in w3cschool.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
						}
		self.home_url = 'https://www.w3cschool.cn/login?refer=/'
		self.login_url = 'https://www.w3cschool.cn/checklogin_1'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	w3cschool().login('', '')