'''
Function:
	QQ空间模拟登录
		--PC端: https://z.qzone.com/download.html
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
import re
import time
import random
import warnings
import requests
from ..utils.misc import *
warnings.filterwarnings('ignore')


'''
Function:
	QQ空间模拟登录
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
class QQZone():
	def __init__(self, **kwargs):
		self.info = 'QQZone'
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
			all_cookies = {}
			self.__initializePC()
			# 获取pt_login_sig
			params = {
						'proxy_url': 'https://qzs.qq.com/qzone/v6/portal/proxy.html',
						'daid': '5',
						'hide_title_bar': '1',
						'low_login': '0',
						'qlogin_auto_login': '1',
						'no_verifyimg': '1',
						'link_target': 'blank',
						'appid': '549000912',
						'style': '22',
						'target': 'self',
						's_url': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
						'pt_qr_app': '手机QQ空间',
						'pt_qr_link': 'https://z.qzone.com/download.html',
						'self_regurl': 'https://qzs.qq.com/qzone/v6/reg/index.html',
						'pt_qr_help_link': 'https://z.qzone.com/download.html',
						'pt_no_auth': '0'
					}
			res = self.session.get(self.xlogin_url, headers=self.headers, verify=False, params=params)
			all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
			pt_login_sig = all_cookies['pt_login_sig']
			# 获得ptqrtoken
			params = {
						'appid': '549000912',
						'e': '2',
						'l': 'M',
						's': '3',
						'd': '72',
						'v': '4',
						't': str(random.random()),
						'daid': '5',
						'pt_3rd_aid': '0'
					}
			res = self.session.get(self.qrshow_url, headers=self.headers, verify=False, params=params)
			all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
			ptqrtoken = self.__decryptQrsig(all_cookies['qrsig'])
			# 保存二维码图片
			saveImage(res.content, os.path.join(self.cur_path, 'qrcode.jpg'))
			showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			self.session.cookies.update(all_cookies)
			# 检测二维码状态
			while True:
				params = {
							'u1': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
							'ptqrtoken': ptqrtoken,
							'ptredirect': '0',
							'h': '1',
							't': '1',
							'g': '1',
							'from_ui': '1',
							'ptlang': '2052',
							'action': '0-0-' + str(int(time.time())),
							'js_ver': '19112817',
							'js_type': '1',
							'login_sig': pt_login_sig,
							'pt_uistyle': '40',
							'aid': '549000912',
							'daid': '5',
							'ptdrvs': 'AnyQUpMB2syC5zV6V4JDelrCvoAMh-HP6Xy5jvKJzHBIplMBK37jV1o3JjBWmY7j*U1eD8quewY_',
							'has_onekey': '1'
						}
				res = self.session.get(self.qrlogin_url, headers=self.headers, verify=False, params=params)
				if '登录成功' in res.text:
					break
				elif '二维码已经失效' in res.text:
					raise RuntimeError('Fail to login, qrcode has expired...')
				time.sleep(2)
			# 登录成功
			all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
			qq_number = re.findall(r'&uin=(.+?)&service', res.text)[0]
			url_refresh = res.text[res.text.find('http'): res.text.find('pt_3rd_aid=0')] + 'pt_3rd_aid=0'
			self.session.cookies.update(all_cookies)
			res = self.session.get(url_refresh, allow_redirects=False, verify=False)
			all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
			self.session.cookies.update(all_cookies)
			removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			print('[INFO]: Account -> %s, login successfully...' % qq_number)
			infos_return = {'username': qq_number}
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in QQZone.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''qrsig转ptqrtoken, hash33函数'''
	def __decryptQrsig(self, qrsig):
		e = 0
		for c in qrsig:
			e += (e << 5) + ord(c)
		return 2147483647 & e
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
						}
		self.xlogin_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?'
		self.qrshow_url = 'https://ssl.ptlogin2.qq.com/ptqrshow?'
		self.qrlogin_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?'
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	QQZone().login()