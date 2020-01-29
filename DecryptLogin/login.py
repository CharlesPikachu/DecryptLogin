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
	def douban(self, username, password, mode='pc', crackvc_func=None, **kwargs):
		return douban.douban().login(username, password, mode, crackvc_func, **kwargs)
	'''微博'''
	def weibo(self, username, password, mode='mobile', crackvc_func=None, **kwargs):
		return weibo.weibo().login(username, password, mode, crackvc_func, **kwargs)
	'''github'''
	def github(self, username, password, mode='pc', crackvc_func=None, **kwargs):
		return github.github().login(username, password, mode, crackvc_func, **kwargs)
	'''网易云音乐'''
	def music163(self, username, password, mode='pc', crackvc_func=None, **kwargs):
		return music163.music163().login(username, password, mode, crackvc_func, **kwargs)
	'''12306'''
	def zt12306(self, username, password, mode='pc', crackvc_func=None, **kwargs):
		return zt12306.zt12306().login(username, password, mode, crackvc_func, **kwargs)
	'''QQ空间'''
	def QQZone(self, username='', password='', mode='mobile', crackvc_func=None, **kwargs):
		return QQZone.QQZone().login(username, password, mode, crackvc_func, **kwargs)
	'''QQ群'''
	def QQQun(self, username='', password='', mode='mobile', crackvc_func=None, **kwargs):
		return QQQun.QQQun().login(username, password, mode, crackvc_func, **kwargs)
	'''QQ安全中心'''
	def QQId(self, username='', password='', mode='mobile', crackvc_func=None, **kwargs):
		return QQId.QQId().login(username, password, mode, crackvc_func, **kwargs)
	'''知乎'''
	def zhihu(self, username, password, mode='pc', crackvc_func=None, **kwargs):
		return zhihu.zhihu().login(username, password, mode, crackvc_func, **kwargs)
	'''B站'''
	def bilibili(self, username, password, mode='pc', crackvc_func=None, **kwargs):
		return bilibili.bilibili().login(username, password, mode, crackvc_func, **kwargs)
	'''今日头条'''
	def toutiao(self, username, password, mode='mobile', crackvc_func=None, **kwargs):
		return toutiao.toutiao().login(username, password, mode, crackvc_func, **kwargs)
	'''Info'''
	def __repr__(self):
		return self.info


'''模拟登录器-仅返回对应平台的实例化类'''
class Loginer():
	def __init__(self, **kwargs):
		self.info = 'Loginer for returning the instantiated platforms.'
	'''豆瓣'''
	def douban(self):
		return douban.douban()
	'''微博'''
	def weibo(self):
		return weibo.weibo()
	'''github'''
	def github(self):
		return github.github()
	'''网易云音乐'''
	def music163(self):
		return music163.music163()
	'''12306'''
	def zt12306(self):
		return zt12306.zt12306()
	'''QQ空间'''
	def QQZone(self):
		return QQZone.QQZone()
	'''QQ群'''
	def QQQun(self):
		return QQQun.QQQun()
	'''QQ安全中心'''
	def QQId(self):
		return QQId.QQId()
	'''知乎'''
	def zhihu(self):
		return zhihu.zhihu()
	'''B站'''
	def bilibili(self):
		return bilibili.bilibili()
	'''今日头条'''
	def toutiao(self, username, password, mode='mobile', crackvc_func=None, **kwargs):
		return toutiao.toutiao()
	'''Info'''
	def __repr__(self):
		return self.info