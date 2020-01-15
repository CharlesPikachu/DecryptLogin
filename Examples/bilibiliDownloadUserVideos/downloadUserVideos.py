'''
Function:
	获得指定用户信息并下载该用户所有视频
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import re
import argparse
import subprocess
import prettytable
from DecryptLogin import login


'''B站类'''
class Bilibili():
	def __init__(self, username, password, **kwargs):
		self.username = username
		self.password = password
		self.session = Bilibili.login(username, password)
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
					}
		self.user_info_url = 'https://api.bilibili.com/x/space/acc/info'
		self.submit_videos_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos'
		self.view_url = 'https://api.bilibili.com/x/web-interface/view'
		self.video_player_url = 'https://api.bilibili.com/x/player/playurl'
	'''运行主程序'''
	def run(self):
		while True:
			userid = input('请输入目标用户ID(例:243766613) ——> ')
			user_info = self.__getUserInfo(userid)
			tb = prettytable.PrettyTable()
			tb.field_names = list(user_info.keys())
			tb.add_row(list(user_info.values()))
			print('获取的用户信息如下:')
			print(tb)
			is_download = input('是否下载该用户的所有视频(y/n, 默认: y) ——> ')
			if is_download == 'y' or is_download == 'yes' or not is_download:
				self.__downloadVideos(userid)
	'''根据userid获得该用户基本信息'''
	def __getUserInfo(self, userid):
		params = {'mid': userid, 'jsonp': 'jsonp'}
		res = self.session.get(self.user_info_url, params=params, headers=self.headers)
		res_json = res.json()
		user_info = {
						'用户名': res_json['data']['name'],
						'性别': res_json['data']['sex'],
						'个性签名': res_json['data']['sign'],
						'用户等级': res_json['data']['level'],
						'生日': res_json['data']['birthday']
					}
		return user_info
	'''下载目标用户的所有视频'''
	def __downloadVideos(self, userid):
		if not os.path.exists(userid):
			os.mkdir(userid)
		# 非会员用户只能下载到高清1080P
		quality = [('16', '流畅 360P'),
				   ('32', '清晰 480P'),
				   ('64', '高清 720P'),
				   ('74', '高清 720P60'),
				   ('80', '高清 1080P'),
				   ('112', '高清 1080P+'),
				   ('116', '高清 1080P60')][-3]
		# 获得用户的视频基本信息
		video_info = {'aids': [], 'cid_parts': [], 'titles': [], 'links': [], 'down_flags': []}
		params = {'mid': userid, 'pagesize': 30, 'tid': 0, 'page': 1, 'order': 'pubdate'}
		while True:
			res = self.session.get(self.submit_videos_url, headers=self.headers, params=params)
			res_json = res.json()
			for item in res_json['data']['vlist']:
				video_info['aids'].append(item['aid'])
			if len(video_info['aids']) < int(res_json['data']['count']):
				params['page'] += 1
			else:
				break
		for aid in video_info['aids']:
			params = {'aid': aid}
			res = self.session.get(self.view_url, headers=self.headers, params=params)
			cid_part = []
			for page in res.json()['data']['pages']:
				cid_part.append([page['cid'], page['part']])
			video_info['cid_parts'].append(cid_part)
			title = res.json()['data']['title']
			title = re.sub(r"[‘’\/\\\:\*\?\"\<\>\|\s']", ' ', title)
			video_info['titles'].append(title)
		print('共获取到用户ID<%s>的<%d>个视频...' % (userid, len(video_info['titles'])))
		for idx in range(len(video_info['titles'])):
			aid = video_info['aids'][idx]
			cid_part = video_info['cid_parts'][idx]
			link = []
			down_flag = False
			for cid, part in cid_part:
				params = {'avid': aid, 'cid': cid, 'qn': quality, 'otype': 'json', 'fnver': 0, 'fnval': 16}
				res = self.session.get(self.video_player_url, params=params, headers=self.headers)
				res_json = res.json()
				if 'dash' in res_json['data']:
					down_flag = True
					v, a = res_json['data']['dash']['video'][0], res_json['data']['dash']['audio'][0]
					link_v = [v['baseUrl']]
					link_a = [a['baseUrl']]
					if v['backup_url']:
						for item in v['backup_url']:
							link_v.append(item)
					if a['backup_url']:
						for item in a['backup_url']:
							link_a.append(item)
					link = [link_v, link_a]
				else:
					link = [res_json['data']['durl'][-1]['url']]
					if res_json['data']['durl'][-1]['backup_url']:
						for item in res_json['data']['durl'][-1]['backup_url']:
							link.append(item)
				video_info['links'].append(link)
				video_info['down_flags'].append(down_flag)
		# 开始下载
		out_pipe_quiet = subprocess.PIPE
		out_pipe = None
		aria2c_path = os.path.join(os.getcwd(), 'tools/aria2c')
		ffmpeg_path = os.path.join(os.getcwd(), 'tools/ffmpeg')
		for idx in range(len(video_info['titles'])):
			title = video_info['titles'][idx]
			aid = video_info['aids'][idx]
			down_flag = video_info['down_flags'][idx]
			print('正在下载视频<%s>...' % title)
			if down_flag:
				link_v, link_a = video_info['links'][idx]
				# --视频
				url = '"{}"'.format('" "'.join(link_v))
				command = '{} -c -k 1M -x {} -d "{}" -o "{}" --referer="https://www.bilibili.com/video/av{}" {} {}'
				command = command.format(aria2c_path, len(link_v), userid, title+'.flv', aid, "", url)
				process = subprocess.Popen(command, stdout=out_pipe, stderr=out_pipe, shell=True)
				process.wait()
				# --音频
				url = '"{}"'.format('" "'.join(link_a))
				command = '{} -c -k 1M -x {} -d "{}" -o "{}" --referer="https://www.bilibili.com/video/av{}" {} {}'
				command = command.format(aria2c_path, len(link_v), userid, title+'.aac', aid, "", url)
				process = subprocess.Popen(command, stdout=out_pipe, stderr=out_pipe, shell=True)
				process.wait()
				# --合并
				command = '{} -i "{}" -i "{}" -c copy -f mp4 -y "{}"'
				command = command.format(ffmpeg_path, os.path.join(userid, title+'.flv'), os.path.join(userid, title+'.aac'), os.path.join(userid, title+'.mp4'))
				process = subprocess.Popen(command, stdout=out_pipe, stderr=out_pipe_quiet, shell=True)
				process.wait()
				os.remove(os.path.join(userid, title+'.flv'))
				os.remove(os.path.join(userid, title+'.aac'))
			else:
				link = video_info['links'][idx]
				url = '"{}"'.format('" "'.join(link))
				command = '{} -c -k 1M -x {} -d "{}" -o "{}" --referer="https://www.bilibili.com/video/av{}" {} {}'
				command = command.format(aria2c_path, len(link), userid, title+'.flv', aid, "", url)
				process = subprocess.Popen(command, stdout=out_pipe, stderr=out_pipe, shell=True)
				process.wait()
				os.rename(os.path.join(userid, title+'.flv'), os.path.join(userid, title+'.mp4'))
		print('所有视频下载完成, 该用户所有视频保存在<%s>文件夹中...' % (userid))
	'''借助我开源的库来登录B站'''
	@staticmethod
	def login(username, password):
		_, session = login.Login().bilibili(username, password)
		return session


'''run'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='下载B站指定用户的所有视频(仅支持Windows下使用)')
	parser.add_argument('--username', dest='username', help='用户名', type=str, required=True)
	parser.add_argument('--password', dest='password', help='密码', type=str, required=True)
	args = parser.parse_args()
	bili = Bilibili(args.username, args.password)
	bili.run()