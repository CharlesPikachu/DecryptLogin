'''
Function:
	微博模拟登录:
		--PC端暂不支持
		--https://m.weibo.cn/(移动端)
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
	微博模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--version: mobile/pc
		Return:
			--session: 登录后的requests.Session()
'''
class weibo():
	def __init__(self, **kwargs):
		self.info = 'weibo'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, version='mobile'):
		if version == 'mobile':
			self.__initializeMobile()
			data = {
					'username': username,
					'password': password,
					'savestate': '1',
					'r': 'https://weibo.cn/',
					'ec': '0',
					'pagerefer': 'https://weibo.cn/pub/',
					'entry': 'mweibo',
					'wentry': '',
					'loginfrom': '',
					'client_id': '',
					'code': '',
					'qq': '',
					'mainpageflag': '1',
					'hff': '',
					'hfp': ''
					}
			res = self.session.post(self.login_url, headers=self.login_headers, data=data)
			if res.json()['retcode'] == 20000000:
				print('[INFO]: Account -> %s, login successfully...' % username)
				return username, self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		elif version == 'pc':
			return None
		else:
			raise ValueError('Unsupport argument in weibo.login -> version %s, expect <mobile> or <pc>...' % version)
	'''初始化PC端'''
	def __initializePC(self):
		pass
	'''初始化移动端'''
	def __initializeMobile(self):
		self.login_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
								'Accept': '*/*',
								'Accept-Encoding': 'gzip, deflate, br',
								'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
								'Connection': 'keep-alive',
								'Origin': 'https://passport.weibo.cn',
								'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
							}
		self.login_url = 'https://passport.weibo.cn/sso/login'


'''test'''
if __name__ == '__main__':
	weibo().login('', '')