'''
Function:
	微博监控
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import re
import time
from DecryptLogin import login


'''微博监控'''
class wbMonitor():
	def __init__(self, username, password, time_interval=30, **kwargs):
		_, self.session = login.Login().weibo(username, password, 'mobile')
		self.headers = {
						'Accept': 'application/json, text/plain, */*',
						'Accept-Encoding': 'gzip, deflate, br',
						'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
						'Connection': 'keep-alive',
						'Host': 'm.weibo.cn',
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
					}
		self.api_url = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value={}&containerid={}'
		self.format_profile_url = 'https://m.weibo.cn/u/{}?uid={}&luicode=10000011&lfid=231093_-_selffollowed'
		self.time_interval = time_interval
	'''开始监控'''
	def start(self, user_id=None):
		if not user_id:
			followed = self.__getFollowed()
			print('未指定想要监控的用户ID, 您关注的用户有:\n(是否想选择其中一位进行监控?)')
			print('-' * 40)
			for idx, each in enumerate(sorted(followed.keys())):
				print('[%d]. %s' % (idx+1, each))
			print('-' * 40)
			while True:
				user_choice = input('请选择您想要监控的用户编号(例如1):')
				try:
					profile_url = followed[sorted(followed.keys())[int(user_choice)-1]]
					user_id = re.findall(r'uid=(\d+)&', profile_url)[0]
					break
				except:
					print('您的输入有误, 请重新输入.')
		else:
			profile_url = self.format_profile_url.format(user_id, user_id)
		self.__monitor(user_id, profile_url)
	'''监控用户主页'''
	def __monitor(self, user_id, profile_url):
		user_name, containerid = self.__getContainerid(user_id, profile_url)
		res = self.session.get(self.api_url.format(user_id, user_id, containerid))
		weibo_ids = []
		cards = res.json()['data']['cards']
		for card in cards:
			if card['card_type'] == 9:
				weibo_ids.append(str(card['mblog']['id']))
		while True:
			weibo_ids = self.__checkUpdate(user_id, profile_url, weibo_ids)
			time.sleep(self.time_interval)
	'''检查用户是否有新的微博'''
	def __checkUpdate(self, user_id, profile_url, weibo_ids):
		user_name, containerid = self.__getContainerid(user_id, profile_url)
		res = self.session.get(self.api_url.format(user_id, user_id, containerid))
		cards = res.json()['data']['cards']
		flag = False
		for card in cards:
			if card['card_type'] == 9:
				if str(card['mblog']['id']) not in weibo_ids:
					flag = True
					weibo_ids.append(str(card['mblog']['id']))
					print(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + ': 用户<%s>发布了新微博' % user_name)
					pics = []
					if card['mblog'].get('pics'):
						for i in card['mblog']['pics']:
							pics.append(i['url'])
					pics = '||'.join(pics)
					print('[时间]: %s\n[来源]: %s\n[原文作者]: %s\n[内容]: %s\n[图片链接]： %s\n' % 
						  (card['mblog']['created_at'], card['mblog']['source'], card['mblog']['user']['screen_name'], card['mblog']['text'], pics))
		if not flag:
			print(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + ': 用户<%s>未发布新微博' % user_name)
		return weibo_ids
	'''获取containerid'''
	def __getContainerid(self, user_id, profile_url):
		self.session.get(profile_url)
		containerid = re.findall(r'fid%3D(\d+)%26', str(self.session.cookies))[0]
		res = self.session.get(self.api_url.format(user_id, user_id, containerid))
		user_name = self.__decode(re.findall(r'"screen_name":"(.*?)"', res.text)[0])
		for i in res.json()['data']['tabsInfo']['tabs']:
			if i['tab_type'] == 'weibo':
				containerid = i['containerid']
		return user_name, containerid
	'''获取关注列表'''
	def __getFollowed(self):
		data = {}
		page = 0
		while True:
			page += 1
			res = self.session.get('https://m.weibo.cn/api/container/getIndex?containerid=231093_-_selffollowed&page={}'.format(page), headers=self.headers)
			profile_urls = re.findall(r'"profile_url":"(.*?)"', res.text)
			screen_names = re.findall(r'"screen_name":"(.*?)"', res.text)
			if len(profile_urls) == 0:
				break
			for screen_name, profile_url in zip(screen_names, profile_urls):
				data[self.__decode(screen_name)] = profile_url.replace('\\', '')
		return data
	'''解码'''
	def __decode(self, content):
		return content.encode('latin-1').decode('unicode_escape')


'''run'''
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="微博监控")
	parser.add_argument('-u', dest='username', help='用户名')
	parser.add_argument('-p', dest='password', help='密码')
	parser.add_argument('-i', dest='id', help='待监控用户id')
	parser.add_argument('-t', dest='time_interval', default=30, type=int, help='监控的时间间隔')
	args = parser.parse_args()
	if args.username and args.password:
		wb = wbMonitor(username=args.username, password=args.password, time_interval=args.time_interval)
		wb.start(args.id)