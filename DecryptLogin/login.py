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
	2020-04-18
'''
from .platforms import *


'''模拟登录-直接登录返回session'''
class Login():
	def __init__(self, **kwargs):
		self.info = 'Login some website using requests.'
		self.__initializeAll()
	'''初始化所有平台'''
	def __initializeAll(self):
		# 豆瓣
		self.douban = douban().login
		# 微博
		self.weibo = weibo().login
		# github
		self.github = github().login
		# 网易云音乐
		self.music163 = music163().login
		# 中国铁路12306
		self.zt12306 = zt12306().login
		# QQ空间
		self.QQZone = QQZone().login
		# QQ群
		self.QQQun = QQQun().login
		# QQ安全中心
		self.QQId = QQId().login
		# 知乎
		self.zhihu = zhihu().login
		# B站
		self.bilibili = bilibili().login
		# 今日头条
		self.toutiao = toutiao().login
		# 淘宝
		self.taobao = taobao().login
		# 京东
		self.jingdong = jingdong().login
		# 凤凰网
		self.ifeng = ifeng().login
		# 搜狐
		self.sohu = sohu().login
		# 中关村在线
		self.zgconline = zgconline().login
		# 拉勾网
		self.lagou = lagou().login
		# 推特
		self.twitter = twitter().login
		# vultr
		self.vultr = vultr().login
		# 天翼
		self.eSurfing = eSurfing().login
		# 人人网
		self.renren = renren().login
		# w3cschool
		self.w3cschool = w3cschool().login
		# 鱼C论坛
		self.fishc = fishc().login
		# 有道
		self.youdao = youdao().login
		# 百度网盘
		self.baidupan = baidupan().login
		# stackoverflow
		self.stackoverflow = stackoverflow().login
		# codalab
		self.codalab = codalab().login
		# pypi
		self.pypi = pypi().login
		# 虾米音乐
		self.xiami = xiami().login
		# 斗鱼直播
		self.douyu = douyu().login
		# 咪咕音乐
		self.migu = migu().login
		# 去哪儿旅行
		self.qunar = qunar().login
		# 小米商城
		self.mieshop = mieshop().login
		# 微信公众号
		self.mpweixin = mpweixin().login
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
		# 豆瓣
		self.douban = douban
		# 微博
		self.weibo = weibo
		# github
		self.github = github
		# 网易云音乐
		self.music163 = music163
		# 中国铁路12306
		self.zt12306 = zt12306
		# QQ空间
		self.QQZone = QQZone
		# QQ群
		self.QQQun = QQQun
		# QQ安全中心
		self.QQId = QQId
		# 知乎
		self.zhihu = zhihu
		# B站
		self.bilibili = bilibili
		# 今日头条
		self.toutiao = toutiao
		# 淘宝
		self.taobao = taobao
		# 京东
		self.jingdong = jingdong
		# 凤凰网
		self.ifeng = ifeng
		# 搜狐
		self.sohu = sohu
		# 中关村在线
		self.zgconline = zgconline
		# 拉勾网
		self.lagou = lagou
		# 推特
		self.twitter = twitter
		# vultr
		self.vultr = vultr
		# 天翼
		self.eSurfing = eSurfing
		# 人人网
		self.renren = renren
		# w3cschool
		self.w3cschool = w3cschool
		# 鱼C论坛
		self.fishc = fishc
		# 有道
		self.youdao = youdao
		# 百度网盘
		self.baidupan = baidupan
		# stackoverflow
		self.stackoverflow = stackoverflow
		# codalab
		self.codalab = codalab
		# pypi
		self.pypi = pypi
		# 虾米音乐
		self.xiami = xiami
		# 斗鱼直播
		self.douyu = douyu
		# 咪咕音乐
		self.migu = migu
		# 去哪儿旅行
		self.qunar = qunar
		# 小米商城
		self.mieshop = mieshop
		# 微信公众号
		self.mpweixin = mpweixin
	'''Info'''
	def __repr__(self):
		return self.info