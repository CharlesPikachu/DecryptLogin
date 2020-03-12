'''
Function:
	微博表情包爬取
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import time
import random
import argparse
import requests
import prettytable
from tqdm import tqdm
from lxml import etree
from DecryptLogin import login
from fake_useragent import UserAgent


'''命令行参数解析'''
def parseArgs():
	parser = argparse.ArgumentParser(description='下载指定微博用户发的所有图片')
	parser.add_argument('--username', dest='username', help='用户名', type=str, required=True)
	parser.add_argument('--password', dest='password', help='密码', type=str, required=True)
	args = parser.parse_args()
	return args


'''微博表情包爬取'''
class weiboEmoji():
	def __init__(self, username, password, **kwargs):
		self.headers = {
							'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
						}
		self.cur_path = os.getcwd()
		self.ua = UserAgent()
		self.session = weiboEmoji.login(username, password)
	'''外部调用'''
	def run(self):
		while True:
			# 使用者输入目标用户的用户ID
			user_id = input('请输入目标用户ID(例如: 2168613091) ——> ')
			# 提取该目标用户的基本信息供使用者确认输入是否有误
			url = f'https://weibo.cn/{user_id}'
			res = self.session.get(url, headers=self.headers)
			selector = etree.HTML(res.content)
			base_infos = selector.xpath("//div[@class='tip2']/*/text()")
			num_wbs, num_followings, num_followers = int(base_infos[0][3: -1]), int(base_infos[1][3: -1]), int(base_infos[2][3: -1])
			num_wb_pages = selector.xpath("//input[@name='mp']")
			num_wb_pages = int(num_wb_pages[0].attrib['value']) if len(num_wb_pages) > 0 else 1
			url = f'https://weibo.cn/{user_id}/info'
			res = self.session.get(url, headers=self.headers)
			selector = etree.HTML(res.content)
			nickname = selector.xpath('//title/text()')[0][:-3]
			# 使用者确认是否要下载该微博用户发的所有图片
			tb = prettytable.PrettyTable()
			tb.field_names = ['用户名', '关注数量', '被关注数量', '微博数量', '微博页数']
			tb.add_row([nickname, num_followings, num_followers, num_wbs, num_wb_pages])
			print('获取的用户信息如下:')
			print(tb)
			is_download = input('是否爬取该微博用户发的所有图片?(y/n, 默认: y) ——> ')
			if is_download == 'y' or is_download == 'yes' or not is_download:
				userinfos = {'user_id': user_id, 'num_wbs': num_wbs, 'num_wb_pages': num_wb_pages}
				savedir = os.path.join(self.cur_path, user_id)
				if not os.path.exists(savedir):
					os.mkdir(savedir)
				self.__downloadImages(userinfos, savedir)
			# 使用者是否要继续下载
			is_continue = input('是否还需下载其他用户的微博数据?(n/y, 默认: n) ——> ')
			if is_continue == 'n' or is_continue == 'no' or not is_continue:
				break
	'''下载所有图片'''
	def __downloadImages(self, userinfos, savedir):
		# 一些必要的信息
		num_wbs = userinfos.get('num_wbs')
		user_id = userinfos.get('user_id')
		num_wb_pages = userinfos.get('num_wb_pages')
		# 提取图片链接并下载图片
		page_block_size = random.randint(1, 5)
		page_block_count = 0
		for page in tqdm(range(1, num_wb_pages+1)):
			# --提取图片链接
			response = self.session.get(f'https://weibo.cn/{user_id}?page={page}', headers=self.headers)
			image_urls = self.__extractImageUrls(response)
			# --下载图片
			for url in image_urls:
				try:
					res = requests.get(url, headers={'user-agent': self.ua.random}, stream=True)
					with open(os.path.join(savedir, url.split('/')[-1]), 'wb') as fp:
						for chunk in res.iter_content(chunk_size=32):
							fp.write(chunk)
					print('[INFO]: Download an image from: ', url)
				except:
					pass
			# --避免给服务器带来过大压力and避免被封, 每爬几页程序就休息一下
			page_block_count += 1
			if page_block_count % page_block_size == 0:
				time.sleep(random.randint(6, 12))
				page_block_size = random.randint(1, 5)
				page_block_count = 0
	'''提取图片链接'''
	def __extractImageUrls(self, response):
		selector = etree.HTML(response.content)
		contents = selector.xpath("//div[@class='c']")
		if contents[0].xpath("div/span[@class='ctt']"):
			for i in range(0, len(contents)-2):
				content = contents[i]
				is_ori = False if len(content.xpath("div/span[@class='cmt']")) > 3 else True
				if is_ori:
					weibo_id = content.xpath('@id')[0][2:]
				else:
					weibo_id = content.xpath("div/a[@class='cc']/@href")[0]
					weibo_id = weibo_id.split('/')[-1].split('?')[0]
				pic_url = f'https://weibo.cn/mblog/pic/{weibo_id}?rl=0'
				more_pics_url = f'https://weibo.cn/mblog/picAll/{weibo_id}?rl=1'
				image_urls = []
				if pic_url in content.xpath('div/a/@href'):
					if more_pics_url in content.xpath('div/a/@href'):
						res = self.session.get(more_pics_url, headers=self.headers)
						selector = etree.HTML(res.content)
						image_urls = selector.xpath('//img/@src')
						image_urls = [u.replace('/thumb180/', '/large/') for u in image_urls]
					else:
						if content.xpath('.//img/@src'):
							for item in content.xpath('div/a'):
								if len(item.xpath('@href')):
									if pic_url == item.xpath('@href')[0]:
										if len(item.xpath('img/@src')):
											image_urls = item.xpath('img/@src')[0]
											image_urls = [image_urls.replace('/wap180/', '/large/')]
											break
		image_urls_correct = []
		for item in image_urls:
			if item.startswith('ttp'):
				image_urls_correct.append('h' + item)
			else:
				image_urls_correct.append(item)
		return image_urls_correct
	'''模拟登录'''
	@staticmethod
	def login(username, password):
		lg = login.Login()
		_, session = lg.weibo(username, password, 'mobile')
		return session


'''run'''
if __name__ == '__main__':
	args = parseArgs()
	spider = weiboEmoji(args.username, args.password)
	spider.run()