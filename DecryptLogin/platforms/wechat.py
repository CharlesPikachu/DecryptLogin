# coding: utf-8
'''
Function:
	微信模拟登录
		--https://wx.qq.com/(PC端)
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2019-03-09
'''
import os
import re
import json
import time
import requests
import xml.dom.minidom
from ..utils.utils import *


'''
Function:
	微信模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--version: mobile/pc
		Return:
			--session: 登录后的requests.Session()
'''
class wechat():
	def __init__(self, **kwargs):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
						}
		self.login_url = 'https://login.weixin.qq.com/jslogin'
		self.qrcode_url = 'https://login.weixin.qq.com/qrcode/{}'
		self.cgibin_url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip={}&uuid={}&_={}'
		self.redirect_uri = None
		self.base_uri = None
		self.session = requests.Session()
		self.cur_path = os.path.abspath(os.path.dirname(__file__))
	'''登录函数'''
	def login(self, username=None, password=None, version='pc'):
		if version == 'mobile':
			return None
		elif version == 'pc':
			uuid = self.__getUUID()
			self.__downloadQRImage(uuid)
			time.sleep(0.1)
			tip = self.__verifyQRcode()
			while True:
				code = self.__isVerifyQR(tip, uuid)
				if code == '200':
					os.remove(os.path.join(self.cur_path, 'vcode.jpg'))
					break
				elif code == '201':
					tip = 0
				elif code == '408':
					raise RuntimeError('Request timed out')
			res = self.session.get(self.redirect_uri)
			content = res.content.decode('utf-8')
			doc = xml.dom.minidom.parseString(content)
			root = doc.documentElement
			skey, wxsid, wxuin, pass_ticket = '', '', '', ''
			for node in root.childNodes:
				if node.nodeName == 'skey':
					skey = node.childNodes[0].data
				elif node.nodeName == 'wxsid':
					wxsid = node.childNodes[0].data
				elif node.nodeName == 'wxuin':
					wxuin = node.childNodes[0].data
				elif node.nodeName == 'pass_ticket':
					pass_ticket = node.childNodes[0].data
			if not all((skey, wxsid, wxuin, pass_ticket)):
				raise RuntimeError('Fail to login, web version of wechat unsupport new registered user to login in...')
			params = {'skey': skey, 'wxsid': wxsid, 'wxuin': wxuin, 'pass_ticket': pass_ticket}
			ret, user, error_msg = self.__initWechat(params)
			if ret == 0:
				print('[INFO]: Account -> %s login successfully...' % user)
				return self.session
			else:
				raise RuntimeError('Fail to initialize wechat, %s...' % error_msg)
		else:
			raise ValueError('Unsupport argument in wechat.login -> version %s, expect <mobile> or <pc>...' % version)
	'''获取uuid, 用于获取登录验证码'''
	def __getUUID(self):
		data = {
					'appid': 'wx782c26e4c19acffb',
					'fun': 'new',
					'lang': 'zh_CN',
					'_': int(time.time())
				}
		res = self.session.get(self.login_url, params=data, headers=self.headers)
		content = res.content.decode('utf-8')
		tmp = re.search(r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"', content)
		code = tmp.group(1)
		uuid = tmp.group(2)
		if code == '200':
			return uuid
		else:
			raise RuntimeError('Fali to get uuid...')
	'''下载验证码'''
	def __downloadQRImage(self, uuid):
		data = {
					't': 'webwx',
					'_': int(time.time())
				}
		res = self.session.get(self.qrcode_url.format(uuid), params=data, headers=self.headers)
		saveImage(res.content, os.path.join(self.cur_path, 'vcode.jpg'))
		return True
	'''二维码验证'''
	def __verifyQRcode(self):
		showImage(os.path.join(self.cur_path, 'vcode.jpg'))
		print('[INFO]: Please use WeChat to scan the QR code to login in...')
		return 1
	'''验证验证码是否被扫描'''
	def __isVerifyQR(self, tip, uuid):
		res = self.session.get(self.cgibin_url.format(tip, uuid, int(time.time())), headers=self.headers)
		content = res.content.decode('utf-8')
		code = re.search(r'window.code=(\d+);', content).group(1)
		if code == '200':
			self.redirect_uri = re.search(r'window.redirect_uri="(\S+?)";', content).group(1) + '&fun=new'
			removeImage(os.path.join(self.cur_path, 'vcode.jpg'))
		return code
	'''微信初始化'''
	def __initWechat(self, **kwargs):
		self.base_uri = self.redirect_uri[:self.redirect_uri.rfind('/')]
		url = self.base_uri + '/webwxinit?pass_ticket={}&skey={}&r={}'.format(kwargs.get('pass_ticket'), kwargs.get('skey'), int(time.time()))
		data = {
					'BaseRequest': {'Uin': int(kwargs.get('wxuin')), 'Sid': kwargs.get('wxsid'), 'Skey': kwargs.get('skey'), 'DeviceID': 'e000000000000000'}
				}
		headers = self.headers
		headers['ContentType'] = 'application/json; charset=UTF-8'
		res = self.session.post(url, data=json.dumps(data))
		content = res.content.decode('utf-8')
		info = json.loads(content)
		user = info['User']
		error_msg = info['BaseResponse']['ErrMsg']
		ret = info['BaseResponse']['Ret']
		return ret, user, error_msg


'''test'''
if __name__ == '__main__':
	wechat().login('pc')