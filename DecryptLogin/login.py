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
	2020-01-14
'''
from .platforms import *


'''模拟登录'''
class Login():
	def __init__(self, **kwargs):
		self.info = 'Login some website using requests.'
	'''豆瓣'''
	def douban(self, username, password, mode='pc'):
		return douban.douban().login(username, password, mode)
	'''微博'''
	def weibo(self, username, password, mode='mobile'):
		return weibo.weibo().login(username, password, mode)
	'''github'''
	def github(self, username, password, mode='pc'):
		return github.github().login(username, password, mode)
	'''网易云音乐'''
	def music163(self, username, password, mode='pc'):
		return music163.music163().login(username, password, mode)
	'''12306'''
	def zt12306(self, username, password, mode='pc'):
		return zt12306.zt12306().login(username, password, mode)
	'''QQ空间'''
	def QQZone(self, username='', password='', mode='mobile'):
		return QQZone.QQZone().login(username, password, mode)
	'''QQ群'''
	def QQQun(self, username='', password='', mode='mobile'):
		return QQQun.QQQun().login(username, password, mode)
	'''QQ安全中心'''
	def QQId(self, username='', password='', mode='mobile'):
		return QQId.QQId().login(username, password, mode)
	'''知乎'''
	def zhihu(self, username, password, mode='pc'):
		return zhihu.zhihu().login(username, password, mode)
	'''B站'''
	def bilibili(self, username, password, mode='pc'):
		return bilibili.bilibili().login(username, password, mode)
	'''Info'''
	def __repr__(self):
		return self.info