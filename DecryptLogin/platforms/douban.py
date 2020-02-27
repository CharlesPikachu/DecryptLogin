'''
Function:
	豆瓣模拟登录
		--PC端: https://www.douban.com/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-02-15
'''
import requests


'''
Function:
	豆瓣模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--mode: mobile/pc
			--crackvcFunc: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
		Return:
			--infos_return: 用户名等信息
			--session: 登录后的requests.Session()
'''
class douban():
	def __init__(self, **kwargs):
		self.info = 'douban'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		if mode == 'mobile':
			return None
		elif mode == 'pc':
			self.__initializePC()
			data = {
					'ck': '20FY',
					'name': username,
					'password': password,
					'remember': 'false',
					'ticket': ''
					}
			res = self.session.post(self.login_url, headers=self.login_headers, data=data)
			res_json = res.json()
			# 登录成功
			if res_json['status'] == 'success':
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账号或密码错误
			elif res_json['status'] == 'failed' and res_json['message'] == 'unmatch_name_password':
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他错误
			else:
				raise RuntimeError(res_json.get('description'))
		else:
			raise ValueError('Unsupport argument in douban.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.login_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
							}
		self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	douban().login('', '')