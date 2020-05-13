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
	2020-05-13
'''
from .platforms import *


'''模拟登录-直接登录返回session'''
class Login():
	def __init__(self, **kwargs):
		self.info = 'Login some website using requests.'
		self.__initializeAll()
	'''初始化所有平台'''
	def __initializeAll(self):
		for key, value in {'douban': douban().login, 'weibo': weibo().login, 'github': github().login, 'music163': music163().login, 
						   'zt12306': zt12306().login, 'QQZone': QQZone().login, 'QQQun': QQQun().login, 'QQId': QQId().login, 
						   'zhihu': zhihu().login, 'bilibili': bilibili().login, 'toutiao': toutiao().login, 'taobao': taobao().login, 
						   'jingdong': jingdong().login, 'ifeng': ifeng().login, 'sohu': sohu().login, 'zgconline': zgconline().login, 
						   'lagou': lagou().login, 'twitter': twitter().login, 'vultr': vultr().login, 'eSurfing': eSurfing().login, 
						   'renren': renren().login, 'w3cschool': w3cschool().login, 'fishc': fishc().login, 'youdao': youdao().login, 
						   'baidupan': baidupan().login, 'stackoverflow': stackoverflow().login, 'codalab': codalab().login, 'pypi': pypi().login, 
						   'xiami': xiami().login, 'douyu': douyu().login, 'migu': migu().login, 'qunar': qunar().login, 
						   'mieshop': mieshop().login, 'mpweixin': mpweixin().login}.items():
			setattr(Login, key, value)
	'''Info'''
	def __repr__(self):
		return self.info


'''模拟登录器-仅返回对应平台的实例化类'''
class Loginer():
	def __init__(self, **kwargs):
		self.info = 'Loginer, returning the instantiated platform loginers.'
		self.__initializeAll()
	'''初始化所有平台'''
	def __initializeAll(self):
		for key, value in {'douban': douban, 'weibo': weibo, 'github': github, 'music163': music163, 
						   'zt12306': zt12306, 'QQZone': QQZone, 'QQQun': QQQun, 'QQId': QQId, 
						   'zhihu': zhihu, 'bilibili': bilibili, 'toutiao': toutiao, 'taobao': taobao, 
						   'jingdong': jingdong, 'ifeng': ifeng, 'sohu': sohu, 'zgconline': zgconline, 
						   'lagou': lagou, 'twitter': twitter, 'vultr': vultr, 'eSurfing': eSurfing, 
						   'renren': renren, 'w3cschool': w3cschool, 'fishc': fishc, 'youdao': youdao, 
						   'baidupan': baidupan, 'stackoverflow': stackoverflow, 'codalab': codalab, 'pypi': pypi, 
						   'xiami': xiami, 'douyu': douyu, 'migu': migu, 'qunar': qunar, 
						   'mieshop': mieshop, 'mpweixin': mpweixin}.items():
			setattr(Loginer, key, value)
	'''Info'''
	def __repr__(self):
		return self.info