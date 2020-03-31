'''
Function:
	CodaLab模拟登录
		--PC端: https://competitions.codalab.org/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-31
'''
import re
import requests


'''
Function:
	CodaLab模拟登录
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
class codalab():
	def __init__(self, **kwargs):
		self.info = 'codalab'
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
			# 获得csrfmiddlewaretoken参数
			res = self.session.get(self.token_url)
			csrfmiddlewaretoken = re.findall(r"name='csrfmiddlewaretoken' value='(.*?)'", res.text)[0]
			# 构造登录请求
			data = {
						'csrfmiddlewaretoken': csrfmiddlewaretoken,
						'login': username,
						'password': password,
						'remember': 'on',
						'next': '/'
					}
			self.session.headers.update({'Referer': self.token_url})
			res = self.session.post(self.login_url, data=data, allow_redirects=False)
			res = self.session.get(self.home_url)
			# 登录成功
			if (res.status_code == 200) and (username in res.text):
				print('[INFO]: Account -> %s, login successfully...' % username)
				user_id = re.findall(r'user_id: (\d+),', res.text)[0]
				email = re.findall(r'email: "(.*?)",', res.text)[0]
				infos_return = {'username': username, 'user_id': user_id, 'email': email}
				return infos_return, self.session
			# 登录失败
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in codalab.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
							'Host': 'competitions.codalab.org'
						}
		self.token_url = 'https://competitions.codalab.org/accounts/login/?next=/'
		self.home_url = 'https://competitions.codalab.org/'
		self.login_url = 'https://competitions.codalab.org/accounts/login/'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	codalab().login('', '')