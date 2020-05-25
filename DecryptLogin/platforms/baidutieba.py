'''
Function:
	百度贴吧模拟登录:
		--PC端暂不支持
		--移动端: https://passport.baidu.com/v3/login/main/qrbdusslogin
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-05-25
'''
import os
import time
import json
import requests
from ..utils.misc import *


'''
Function:
	百度贴吧模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--mode: mobile/pc
			--crackvcFunc: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
			--proxies: 为requests.Session()设置代理
		Return:
			--infos_return: 用户名等信息
			--session: 登录后的requests.Session()
'''
class baidutieba():
	def __init__(self, **kwargs):
		self.info = 'baidutieba'
		self.cur_path = os.getcwd()
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username='', password='', mode='pc', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			raise NotImplementedError
		# PC端接口
		elif mode == 'pc':
			self.__initializePC()
			# 获得登录二维码
			timestamp = str(int(time.time() * 1000))
			params = {
						'lp': 'pc',
						'qrloginfrom': 'pc',
						'apiver': 'v3',
						'tt': timestamp,
						'tpl': 'tb',
						'_': timestamp
					}
			res = self.session.get(self.getqrcode_url, params=params)
			imgurl = res.json()['imgurl']
			sign = res.json()['sign']
			res = self.session.get('https://%s' % imgurl)
			saveImage(res.content, os.path.join(self.cur_path, 'qrcode.jpg'))
			showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			# 检测二维码状态
			while True:
				timestamp = str(int(time.time() * 1000))
				params = {
							'channel_id': sign,
							'tpl': 'tb',
							'apiver': 'v3',
							'callback': '',
							'tt': timestamp,
							'_': timestamp
						}
				res = self.session.get(self.unicast_url, params=params)
				res_json = json.loads(res.text.replace('(', '').replace(')', ''))
				# --二维码失效或请求有误
				if 'channel_v' not in res_json:
					raise RuntimeError('Fail to login, qrcode has expired or something error when fetching qrcode status...')
				# --正在扫码
				elif json.loads(res_json['channel_v'])['status'] in [1]:
					pass
				# --扫码成功
				elif json.loads(res_json['channel_v'])['status'] in [0]:
					timestamp = str(int(time.time() * 1000))
					res_json = json.loads(res_json['channel_v'])
					params = {
								'v': timestamp,
								'bduss': res_json['v'],
								'u': 'https://tieba.baidu.com/index.html',
								'loginVersion': 'v4',
								'qrcode': '1',
								'tpl': 'tb',
								'apiver': 'v3',
								'tt': timestamp,
								'alg': 'v1',
								'time': timestamp[10:]
							}
					res = self.session.get(self.login_url, params=params)
					res_json = json.loads(res.text.replace("'", '"'))
					self.session.get(self.crossdomain_url+'?bdu=%s&t=%s' % (res_json['data']['hao123Param'], timestamp))
					res = self.session.get(self.userinfo_url)
					res_json['userinfo'] = res.json()
					username = res_json['userinfo']['data']['user_name_show']
					break
			# 登录成功
			removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			print('[INFO]: Account -> %s, login successfully...' % username)
			infos_return = {'username': username}
			infos_return.update(res_json)
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in baidutieba.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
					}
		self.getqrcode_url = 'https://passport.baidu.com/v2/api/getqrcode'
		self.unicast_url = 'https://passport.baidu.com/channel/unicast'
		self.login_url = 'https://passport.baidu.com/v3/login/main/qrbdusslogin'
		self.crossdomain_url = 'https://user.hao123.com/static/crossdomain.php'
		self.userinfo_url = 'https://tieba.baidu.com/f/user/json_userinfo'
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	baidutieba().login('', '')