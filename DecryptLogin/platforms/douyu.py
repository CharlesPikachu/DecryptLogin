'''
Function:
	斗鱼直播模拟登录
		--PC端: https://www.douyu.com/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-04-06
'''
import os
import re
import time
import json
import qrcode
import requests
from ..utils.misc import *


'''
Function:
	QQ群模拟登录
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
class douyu():
	def __init__(self, **kwargs):
		self.info = 'douyu'
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
			# 获取登录二维码
			res = self.session.post(self.gen_qrcode_url, data={'client_id': '1'})
			res_json = res.json()
			if res_json['error'] != 0:
				raise RuntimeError('Fail to login, unable to fetch url of qrcode...')
			code = res_json['data']['code']
			scan_url = res_json['data']['url'].replace('\\', '')
			# 保存并显示登录二维码(这里需要把获得的scan_url转成登录二维码)
			qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
			qr.add_data(scan_url)
			qr.make(fit=True)
			img = qr.make_image(fill_color="black", back_color="white")
			img.save(os.path.join(self.cur_path, 'qrcode.jpg'))
			showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			# 检测二维码状态
			while True:
				res = self.session.get(self.check_url.format(timestamp=str(int(time.time()*1000)), code=code))
				res_json = res.json()
				# --扫码成功
				if res_json['error'] == 0:
					login_url = 'https:' + res_json['data']['url']
					params = {
								'callback': 'appClient_json_callback',
								'_': str(int(time.time()*1000))
							}
					res = self.session.get(login_url, params=params)
					res_json = json.loads(res.text.replace('appClient_json_callback(', '')[:-1])
					if res_json['error'] != 0:
						raise ValueError(res_json['msg'])
					break
				# --等待扫码以及正在扫码
				elif res_json['error'] in [-2, 1]:
					pass
				# --二维码过期
				elif res_json['error'] == -1:
					raise RuntimeError('Fail to login, qrcode has expired...')
				# --其他原因
				else:
					raise RuntimeError(res_json['data'])
				time.sleep(0.5)
			# 登录成功
			removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			res = self.session.get(self.member_url)
			username = re.findall(r'uname_con clearfix" title="(.*?)"', res.text)[0]
			print('[INFO]: Account -> %s, login successfully...' % username)
			infos_return = {'username': username}
			infos_return.update(res_json)
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in douyu.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
						'Referer': 'https://passport.douyu.com/index/login?passport_reg_callback=PASSPORT_REG_SUCCESS_CALLBACK&passport_login_callback=PASSPORT_LOGIN_SUCCESS_CALLBACK&passport_close_callback=PASSPORT_CLOSE_CALLBACK&passport_dp_callback=PASSPORT_DP_CALLBACK&type=login&client_id=1&state=https%3A%2F%2Fwww.douyu.com%2F'
					}
		self.gen_qrcode_url = 'https://passport.douyu.com/scan/generateCode'
		self.check_url = 'https://passport.douyu.com/lapi/passport/qrcode/check?time={timestamp}&code={code}'
		self.member_url = 'https://www.douyu.com/member'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	douyu().login()