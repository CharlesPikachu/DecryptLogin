# coding: utf-8
'''
Function:
	GitHub模拟登录
		--https://github.com/(PC端)
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2019-03-04
'''
import re
import requests


'''
Function:
	GitHub模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--version: mobile/pc
		Return:
			--session: 登录后的requests.Session()
'''
class github():
	def __init__(self, **kwargs):
		self.login_headers = {
								'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
								'Accept-Encoding': 'gzip, deflate, br',
								'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
								'Cache-Control': 'no-cache',
								'Connection': 'keep-alive',
								'Content-Length': '196',
								'Content-Type': 'application/x-www-form-urlencoded',
								'Host': 'github.com',
								'Origin': 'https://github.com',
								'Pragma': 'no-cache',
								'Referer': 'https://github.com/login',
								'Upgrade-Insecure-Requests': '1',
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
							}
		self.login_url = 'https://github.com/login'
		self.post_url = 'https://github.com/session'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, version='pc'):
		if version == 'mobile':
			return None
		elif version == 'pc':
			token = self.__getToken()
			data = {
					'commit': 'Sign in',
					'utf8': '✓',
					'authenticity_token': token,
					'login': username,
					'password': password
					}
			res = self.session.post(self.post_url, headers=self.login_headers, data=data)
			if res.status_code == 200 and 'Sign in to GitHub · GitHub' not in res.text:
				print('[INFO]: Account -> %s, login successfully...' % username)
				return self.session
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in github.login -> version %s, expect <mobile> or <pc>...' % version)
	'''获取authenticity_token参数'''
	def __getToken(self):
		res = self.session.get(self.login_url)
		token = re.findall(r'authenticity_token.*?value="(.*?)"', res.text)[0]
		return token


'''test'''
if __name__ == '__main__':
	github().login('', '')