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
	2020-01-29
'''
from .platforms import *


'''模拟登录-直接登录返回session'''
class Login():
	def __init__(self, **kwargs):
		self.info = 'Login some website using requests.'
	'''豆瓣'''
	def douban(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		return douban.douban().login(username, password, mode, crackvcFunc, **kwargs)
	'''微博'''
	def weibo(self, username, password, mode='mobile', crackvcFunc=None, **kwargs):
		return weibo.weibo().login(username, password, mode, crackvcFunc, **kwargs)
	'''github'''
	def github(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		return github.github().login(username, password, mode, crackvcFunc, **kwargs)
	'''网易云音乐'''
	def music163(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		return music163.music163().login(username, password, mode, crackvcFunc, **kwargs)
	'''12306'''
	def zt12306(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		return zt12306.zt12306().login(username, password, mode, crackvcFunc, **kwargs)
	'''QQ空间'''
	def QQZone(self, username='', password='', mode='mobile', crackvcFunc=None, **kwargs):
		return QQZone.QQZone().login(username, password, mode, crackvcFunc, **kwargs)
	'''QQ群'''
	def QQQun(self, username='', password='', mode='mobile', crackvcFunc=None, **kwargs):
		return QQQun.QQQun().login(username, password, mode, crackvcFunc, **kwargs)
	'''QQ安全中心'''
	def QQId(self, username='', password='', mode='mobile', crackvcFunc=None, **kwargs):
		return QQId.QQId().login(username, password, mode, crackvcFunc, **kwargs)
	'''知乎'''
	def zhihu(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		return zhihu.zhihu().login(username, password, mode, crackvcFunc, **kwargs)
	'''B站'''
	def bilibili(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		return bilibili.bilibili().login(username, password, mode, crackvcFunc, **kwargs)
	'''今日头条'''
	def toutiao(self, username, password, mode='mobile', crackvcFunc=None, **kwargs):
		return toutiao.toutiao().login(username, password, mode, crackvcFunc, **kwargs)
	'''Info'''
	def __repr__(self):
		return self.info


'''模拟登录器-仅返回对应平台的实例化类'''
class Loginer():
	def __init__(self, **kwargs):
		self.info = 'Loginer for returning the instantiated platforms.'
	'''豆瓣'''
	def douban(self, **kwargs):
		return douban.douban(**kwargs)
	'''微博'''
	def weibo(self, **kwargs):
		return weibo.weibo(**kwargs)
	'''github'''
	def github(self, **kwargs):
		return github.github(**kwargs)
	'''网易云音乐'''
	def music163(self, **kwargs):
		return music163.music163(**kwargs)
	'''12306'''
	def zt12306(self, **kwargs):
		return zt12306.zt12306(**kwargs)
	'''QQ空间'''
	def QQZone(self, **kwargs):
		return QQZone.QQZone(**kwargs)
	'''QQ群'''
	def QQQun(self, **kwargs):
		return QQQun.QQQun(**kwargs)
	'''QQ安全中心'''
	def QQId(self, **kwargs):
		return QQId.QQId(**kwargs)
	'''知乎'''
	def zhihu(self, **kwargs):
		return zhihu.zhihu(**kwargs)
	'''B站'''
	def bilibili(self, **kwargs):
		return bilibili.bilibili(**kwargs)
	'''今日头条'''
	def toutiao(self, **kwargs):
		return toutiao.toutiao(**kwargs)
	'''Info'''
	def __repr__(self):
		return self.info