'''
Function:
	推特模拟登录:
		--PC端: https://twitter.com/login
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
import re
import requests


'''
Function:
	推特模拟登录
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
class twitter():
	def __init__(self, **kwargs):
		self.info = 'twitter'
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			raise NotImplementedError
		# PC端接口
		elif mode == 'pc':
			self.__initializePC()
			# 访问home_url
			res = self.session.get(self.home_url)
			pattern = re.compile(r'<input type="hidden" value="(.*?)" name="authenticity_token">')
			authenticity_token = re.findall(pattern, res.text)[0]
			# 访问login_url进行模拟登录
			data = {
						'redirect_after_login': '/',
						'authenticity_token': authenticity_token,
						'scribe_log': '',
						'return_to_ssl': 'true',
						'session[username_or_email]': username,
						'session[password]': password
					}
			res = self.session.post(self.login_url, data=data, headers=self.headers)
			res_text = res.text.replace('&quot', '').replace(';', '')
			# 登录过于频繁时, 需要验证是否为机器人
			if 'Pass a Google reCAPTCHA challenge' in res_text:
				raise RuntimeError('Account -> %s, fail to login, you are suspected of being a robot and have to Pass a Google reCAPTCHA challenge in browser...' % username)
			# 在返回信息中提取有用的信息
			pattern = re.compile(r'<input type="hidden" id="init-data" class="json-data" value="(.*?)"')
			res_text = re.findall(pattern, res_text)[0]
			token, logged_in, screen_name, full_name, user_id, guest_id = re.findall(r'formAuthenticityToken:(.*?),loggedIn:(.*?),screenName:(.*?),fullName:(.*?),userId:(.*?),guestId:(.*?),', res_text)[0]
			res_json = {'formAuthenticityToken': token, 'screenName': screen_name, 'fullName': full_name, 'userId': user_id, 'guestId': guest_id}
			# 登录成功
			if logged_in == 'true':
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 登录失败
			else:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
		else:
			raise ValueError('Unsupport argument in twitter.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
						'Content-Type': 'application/x-www-form-urlencoded',
						'Origin': 'https://twitter.com',
						'Referer': 'https://twitter.com/login'
					}
		self.home_url = 'https://twitter.com/'
		self.login_url = 'https://twitter.com/sessions'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	twitter().login('', '')