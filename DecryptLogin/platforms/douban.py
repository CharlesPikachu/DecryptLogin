'''
Function:
	豆瓣模拟登录
		--https://www.douban.com/(PC端)
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2019-12-08
'''
import requests


'''
Function:
	豆瓣模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--version: mobile/pc
		Return:
			--session: 登录后的requests.Session()
'''
class douban():
	def __init__(self, **kwargs):
		self.info = 'douban'
		self.session = requests.Session()
		self.username = username
	'''登录函数'''
	def login(self, username, password, version='pc'):
		if version == 'mobile':
			return None
		elif version == 'pc':
			self.username = username
			self.__initializePC()
			data = {
					'ck': '20FY',
					'name': username,
					'password': password,
					'remember': 'false',
					'ticket': ''
					}
			res = self.session.post(self.login_url, headers=self.login_headers, data=data)
			res.encoding = 'gbk'
			if res.json()['status'] == 'success':
				print('[INFO]: Account -> %s, login successfully...' % username)
				return self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in douban.login -> version %s, expect <mobile> or <pc>...' % version)
	'''初始化PC端'''
	def __initializePC(self):
		self.login_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
							}
		self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	douban().login('', '')