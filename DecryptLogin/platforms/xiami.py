'''
Function:
	虾米音乐模拟登录
		--PC端: https://www.xiami.com/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-04-02
'''
import time
import json
import requests
from hashlib import md5


'''
Function:
	有道模拟登录
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
class xiami():
	def __init__(self, **kwargs):
		self.info = 'xiami'
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
			# 获得请求所需的token
			token = self.__getToken()
			# 模拟登录
			login_url = self.base_url.format(action=self.actions['login'])
			params = {
						'account': username,
						'password': md5(password.encode('utf-8')).hexdigest()
					}
			res = self.session.get(login_url, params=self.__xiamiSign(params, token))
			res_json = res.json()
			code, msg = res_json['ret'][0].split('::')
			# 登录成功
			if code == 'SUCCESS':
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账号密码错误
			elif code in ['FAIL_BIZ_GLOBAL_WRONG_PARAMS', 'FAIL_BIZ_GLOBAL_APPLICATION_ERROR']:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他原因
			else:
				raise RuntimeError(msg)
		else:
			raise ValueError('Unsupport argument in xiami.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''虾米签名'''
	def __xiamiSign(self, params, token='', access_token=None):
		appkey = '23649156'
		t = str(int(time.time() * 1000))
		request_str = {
						'header': {'appId': '200', 'platformId': 'h5'},
						'model': params
					}
		if access_token: request_str['header']['accessToken'] = access_token
		data = json.dumps({'requestStr': json.dumps(request_str)})
		sign = '%s&%s&%s&%s' % (token, t, appkey, data)
		sign = md5(sign.encode('utf-8')).hexdigest()
		params = {
					't': t,
					'appKey': appkey,
					'sign': sign,
					'data': data
				}
		return params
	'''获得请求所需的token'''
	def __getToken(self):
		action = self.actions['getsongdetail']
		url = self.base_url.format(action=action)
		params = {'songId': '1'}
		response = self.session.get(url, params=self.__xiamiSign(params))
		cookies = response.cookies.get_dict()
		return cookies['_m_h5_tk'].split('_')[0]
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'Accept': '*/*',
						'Accept-Encoding': 'gzip,deflate,sdch',
						'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
						'Connection': 'keep-alive',
						'Referer': 'http://h.xiami.com',
						'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
					}
		self.base_url = 'https://h5api.m.xiami.com/h5/{action}/1.0/'
		self.actions = {
						'getsongdetail': 'mtop.alimusic.music.songservice.getsongdetail',
						'login': 'mtop.alimusic.xuser.facade.xiamiuserservice.login',
						'getuserinfobyuserid': 'mtop.alimusic.xuser.facade.xiamiuserservice.getuserinfobyuserid'
					}
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	xiami().login('', '')