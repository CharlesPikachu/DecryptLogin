'''
Function:
	requests模拟登录
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2019-12-07
'''
try:
	from .platforms import *
except:
	from platforms import *


'''模拟登录'''
class Login():
	def __init__(self, **kwargs):
		self.info = 'Login some website using requests.'
	'''豆瓣'''
	def douban(self, username, password, version='pc'):
		return douban.douban().login(username, password, version)
	'''微博'''
	def weibo(self, username, password, version='mobile'):
		return weibo.weibo().login(username, password, version)
	'''github'''
	def github(self, username, password, version='pc'):
		return github.github().login(username, password, version)
	'''网易云音乐'''
	def music163(self, username, password, version='pc'):
		return music163.music163().login(username, password, version)
	'''12306'''
	def zt12306(self, username, password, version='pc'):
		return zt12306.zt12306().login(username, password, version)
	'''QQ空间'''
	def QQZone(self, username='', password='', version='mobile'):
		return QQZone.QQZone().login(username, password)
	'''QQ群'''
	def QQQun(self, username='', password='', version='mobile'):
		return QQQun.QQQun().login(username, password)
	'''QQ安全中心'''
	def QQId(self, username='', password='', version='mobile'):
		return QQId.QQId().login(username, password)
	'''Info'''
	def __repr__(self):
		return self.info