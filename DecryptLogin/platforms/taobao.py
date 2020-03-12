'''
Function:
	淘宝模拟登录:
		--PC端: https://login.taobao.com/member/login.jhtml
		--移动端: 暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-29
'''
import re
import time
import random
import requests
from ..utils.misc import *
from urllib.parse import unquote


'''
Function:
	淘宝模拟登录
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
class taobao():
	def __init__(self, **kwargs):
		self.info = 'taobao'
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
			umid_token = self.__generateUmidToken()
			# 请求login_url
			res = self.session.get(self.login_url)
			# 转二维码登录
			res = self.session.get(self.getqr_login_url.format(umid_token))
			res_json = res.json()
			if res_json['success']:
				xcode_url = res_json.get('url', '')
				lg_token = res_json.get('lgToken', '')
			else:
				raise RuntimeError('Fail to login, unable to fetch url of qrcode...')
			# 获取二维码
			res = self.session.get('https:'+xcode_url)
			if not (res.status_code == 200):
				raise RuntimeError('Fail to login, unable to download qrcode from %s...' % xcode_url)
			saveImage(res.content, os.path.join(self.cur_path, 'qrcode.jpg'))
			showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			# 检测二维码状态
			self.session.headers.update({'Referer': 'https://login.taobao.com/member/login_unusual.htm?user_num_id=2979250577&is_ignore=&from=tbTop&style=\
													 &popid=&callback=&minipara=&css_style=&is_scure=true&c_is_secure=&tpl_redirect_url=https%3A%2F%2Fwww.\
													 taobao.com%2F&cr=https%3A%2F%2Fwww.taobao.com%2F&trust_alipay=&full_redirect=&need_sign=&not_duplite_str\
													 =&from_encoding=&sign=&timestamp=&sr=false&guf=&sub=false&wbp=&wfl=null&allp=&loginsite=0&login_type=11&lang\
													 =zh_CN&appkey=00000000&param=7nmIF0VTf6m%2Bbx8wuCmPLTEdh1Ftef8%2B5yUA%2FXNtAI%2FfMwadkeaCast40u2Ng0%2FC7Z75s\
													 OSVLMugWTqKjJ7aA55JYIL%2FPDFJ7zaJhq9XSVUOX%2B1AxQatuIvw4TXGJm1VG4alZ2UohVAAt5WTLYbs5im077nTG%2BOkovORQNtMCEzWKM\
													 e0xcuienFAhsBhC0V7qIYZJvPGOOEt0tORA8Fv1zYPuOkWEPDFsPwYG5xj4LTKNZt5HSRRHkviiPy9AJ9uC%2Bs7V%2FQ7b6K07YUG1fA3tFwAL\
													 GnorSUXRdhcXUBBAt6IiyStIkWFWDgJEymOAXOS5RNGlO1EL5ppmpQas7BarrW2Krui4bxV81AJXyxLfnk3MOxI2dUNdO9VQNY0F6a6nk%2FCzUfR\
													 0NfPRrIoXuZDn2N01A8q5XGrMlWmBCH5%2FSKz6%2F%2BrUx3%2FxQTYWmgV49rVSdtySIHip5PsrXHWXCbHqscdve540l5CUKTT7znsoL45pth%2FosxMUb649Yw1EPAq'})
			while True:
				res = self.session.get(self.checkqr_login_url.format(lg_token))
				res_json = res.json()
				# --扫码成功
				if res_json['code'] == '10006':
					# ----检查是否需要安全验证
					res = self.session.get(res_json.get('url', '') + '&umid_token={}'.format(umid_token))
					if res.url.find('login_unusual.htm') > -1:
						raise RuntimeError('Fail to login, your account requires security verification...')
					uid, token = re.findall(r'uid=(.*?)&token=(.*?)&', res_json.get('url'))[0]
					username = unquote(uid.replace('cntaobao', ''))
					break
				# --二维码已经失效
				elif res_json['code'] == '10004':
					raise RuntimeError('Fail to login, qrcode has expired...')
				# --正在扫码或其他原因
				elif res_json['code'] in ['10001', '10000']:
					pass
				time.sleep(1)
			# 登录成功
			removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
			print('[INFO]: Account -> %s, login successfully...' % username)
			infos_return = {'username': username, 'uid': uid, 'token': token}
			infos_return.update(res_json)
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in taobao.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''生成umidToken'''
	def __generateUmidToken(self):
		umid_token = 'C' + str(int(time.time() * 1000))
		umid_token += ''.join(str(random.choice(range(10))) for _ in range(11))
		umid_token += str(int(time.time() * 1000))
		umid_token += ''.join(str(random.choice(range(10))) for _ in range(3))
		return umid_token
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
						}
		self.login_url = 'https://login.taobao.com/member/login.jhtml?allp=&wbp=&sub=false&sr=false&c_is_scure=&from=tbTop&type=1&style=&minipara=&css_style=&tpl_redirect_url=\
						  https%3A//www.taobao.com&popid=&callback=&is_ignore=&trust_alipay=&full_redirect=&need_sign=&sign=&timestamp=&from_encoding=&qrLogin=&keyLogin=&newMini2='
		self.getqr_login_url = 'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tb&appkey=00000000&umid_token={}'
		self.checkqr_login_url = 'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={}&defaulturl=https://www.taobao.com'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	taobao().login('', '')