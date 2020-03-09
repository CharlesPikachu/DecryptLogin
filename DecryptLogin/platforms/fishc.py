'''
Function:
	鱼C论坛模拟登录
		--PC端: https://fishc.com.cn/forum.php
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-09
'''
import re
import requests
from hashlib import md5


'''
Function:
	鱼C论坛模拟登录
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
class fishc():
	def __init__(self, **kwargs):
		self.info = 'fishc'
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
			# 模拟登录
			data = {
						'username': username,
						'password': md5(password.encode(encoding='utf-8')).hexdigest(),
						'quickforward': 'yes',
						'handlekey': 'ls'
					}
			res = self.session.post(self.login_url, headers=self.login_headers, data=data)
			# 登录失败
			if (u'登录失败' in res.text) or (u'密码错误次数过多' in res.text):
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 登录成功, 跳转到主页提取一些必要的信息
			res = self.session.get(self.home_url)
			uid = re.findall(r"discuz_uid = '(\d+)',", res.text)[0]
			nickname = re.findall(r'title="访问我的空间">(.*?)</a>', res.text)[0]
			print('[INFO]: Account -> %s, login successfully...' % username)
			infos_return = {'username': username, 'nickname': nickname, 'uid': uid}
			return infos_return, self.session
		else:
			raise ValueError('Unsupport argument in fishc.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
		self.login_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
								'Host': 'fishc.com.cn',
								'Origin': 'https://fishc.com.cn',
								'Referer': 'https://fishc.com.cn/'
							}
		self.home_url = 'https://fishc.com.cn/'
		self.login_url = 'https://fishc.com.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	fishc().login('', '')