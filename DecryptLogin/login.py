'''
Function:
	模拟登录
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2019-03-04
'''
from platforms import *


'''模拟登录'''
class Login():
	def __init__(self, **kwargs):
		self.info = 'Login some website using requests, support douban, weibo and gitHub now.'
	def douban(self, username, password, version='pc'):
		return douban.douban().login(username, password, version)
	def weibo(self, username, password, version='mobile'):
		return weibo.weibo().login(username, password, version)
	def github(self, username, password, version='pc'):
		return github.github().login(username, password, version)
	def __repr__(self):
		return self.info


'''test'''
if __name__ == '__main__':
	l = Login()
	print(l)