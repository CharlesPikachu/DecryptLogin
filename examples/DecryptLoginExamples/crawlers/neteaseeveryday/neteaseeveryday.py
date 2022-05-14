'''
Function:
    在终端看网易云每日歌曲推荐
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import re
import time
import click
from pick import pick
from DecryptLogin import login
from contextlib import closing
from DecryptLogin.modules.core.music163 import Cracker


'''在终端看网易云每日歌曲推荐'''
class NeteaseEveryday():
    def __init__(self, username='charlespikachu'):
        self.username = username
        self.session = self.login()
        self.csrf = re.findall('__csrf=(.*?) for', str(self.session.cookies))[0]
        self.cracker = Cracker()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept': '*/*'
        }
        self.clear()
    '''外部调用'''
    def run(self):
        daily_recommend_infos = self.getdailyrecommend()
        keys, values = list(daily_recommend_infos.keys()), list(daily_recommend_infos.values())
        title = '你的网易云每日歌曲推荐如下:'
        options = [v[0] for v in values]
        while True:
            option, index = pick(options, title, indicator='=>')
            self.downloadSong(keys[index], option, values[index][1])
            self.clear()
    '''下载某首歌曲'''
    def downloadSong(self, songid, songname, brs, savedir='.'):
        play_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        self.logging('正在下载 ——> %s' % songname)
        for br in brs:
            data = {
                'ids': [songid],
                'br': br,
                'csrf_token': self.csrf
            }
            response = self.session.post(play_url+self.csrf, headers=self.headers, data=self.cracker.get(data))
            if response.json()['code'] == 200:
                download_url = response.json()['data'][0].get('url', '')
                if download_url:
                    break
        with closing(self.session.get(download_url, headers=self.headers, stream=True, verify=False)) as response:
            total_size = int(response.headers['content-length'])
            if response.status_code == 200:
                label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
                with click.progressbar(length=total_size, label=label) as progressbar:
                    with open(os.path.join(savedir, self.filterBadCharacter(songname)+'.'+download_url.split('.')[-1].split('?')[0]), "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                progressbar.update(1024)
    '''获得每日歌曲推荐'''
    def getdailyrecommend(self):
        url = 'http://music.163.com/weapi/v2/discovery/recommend/songs?csrf_token='
        data = {
            'crsf_token': self.csrf,
            'limit': '999',
            'offset': '0',
            'total': 'true'
        }
        data = self.cracker.get(data)
        response = self.session.post(url, headers=self.headers, data=data)
        response_json = response.json()
        daily_recommend_infos = {}
        if response_json['code'] == 200:
            for item in response_json['recommend']:
                songname = item['name']
                songid = item['id']
                singer = item['artists'][0]['name']
                h = item['hMusic'].get('bitrate', 320000) if item['hMusic'] else 320000
                m = item['mMusic'].get('bitrate', 192000) if item['mMusic'] else 192000
                l = item['lMusic'].get('bitrate', 128000) if item['lMusic'] else 128000
                brs = [h, m, l]
                daily_recommend_infos[songid] = ['%s By %s' % (songname, singer), brs]
            return daily_recommend_infos
        else:
            raise RuntimeError('获取每日歌曲推荐失败, 请检查网络并重新运行程序')
    '''清屏'''
    def clear(self):
        try:
            os.system('cls')
        except:
            os.system('clear')
    '''清除可能出问题的字符'''
    def filterBadCharacter(self, string):
        need_removed_strs = ['<em>', '</em>', '<', '>', '\\', '/', '?', ':', '"', '：', '|', '？', '*']
        for item in need_removed_strs:
            string = string.replace(item, '')
        try:
            rule = re.compile(u'[\U00010000-\U0010ffff]')
        except:
            rule = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        string = rule.sub('', string)
        return string.strip().encode('utf-8', 'ignore').decode('utf-8')
    '''模拟登录'''
    def login(self):
        client = login.Client()
        music163 = client.music163(reload_history=True)
        infos_return, session = music163.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')