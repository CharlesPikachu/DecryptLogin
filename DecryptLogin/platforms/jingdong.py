'''
Function:
	京东模拟登录:
		--PC端: https://www.jd.com/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-29
'''
import os
import time
import json
import requests
from ..utils.misc import *
from urllib.parse import unquote


'''
Function:
	京东模拟登录
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
class jingdong():
	def __init__(self, **kwargs):
		self.info = 'jingdong'
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
			# 获取二维码
			res = self.session.get(self.qrshow_url.format(int(time.time()*1000)))
			saveImage(res.content, os.path.join(self.cur_path, 'qrcode.jpg'))
			showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			# 检测二维码状态
			token = self.session.cookies.get('wlfstk_smdl')
			while True:
				res = self.session.get(self.token_url.format(token))
				res_json = json.loads(res.text[2: -1])
				# --扫码成功
				if res_json['code'] == 200:
					ticket = res_json['ticket']
					res = self.session.get(self.ticket_url.format(ticket))
					res_json = res.json()
					if not res_json['returnCode']:
						res = self.session.get(res_json['url'])
					username = self.session.cookies.get('pin', '')
					nickname = unquote(self.session.cookies.get('unick', ''))
					break
				# --等待扫码以及正在扫码
				elif res_json['code'] in [201, 202]:
					pass
				# --二维码过期
				elif res_json['code'] == 203:
					raise RuntimeError('Fail to login, qrcode has expired...')
				# --其他情况
				else:
					raise RuntimeError(res_json['msg'])
				time.sleep(1)
			# 登录成功
			removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			print('[INFO]: Account -> %s, login successfully...' % nickname)
			infos_return = {'username': username, 'nickname': nickname}
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in alipay.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
						'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
					}
		self.qrshow_url = 'https://qr.m.jd.com/show?appid=133&size=147&t={}'
		self.token_url = 'https://qr.m.jd.com/check?callback=a&isNewVersion=1&_format_=json&appid=133&token={}'
		self.ticket_url = 'https://passport.jd.com/uc/qrCodeTicketValidation?t={}'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	jingdong().login('', '')