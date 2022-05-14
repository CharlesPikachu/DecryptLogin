'''
Function:
    下载网易云音乐登录用户创建/收藏的歌单内所有歌曲
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import re
import time
import click
import prettytable
from contextlib import closing
from DecryptLogin import login
from DecryptLogin.modules.core.music163 import Cracker


'''下载器类'''
class NeteaseSongListDownloader():
    def __init__(self, username='charlespikachu'):
        self.username = username
        infos_return, self.session = self.login()
        self.userid = infos_return['response'].get('account', {}).get('id')
        self.csrf = re.findall('__csrf=(.*?) for', str(self.session.cookies))[0]
        self.cracker = Cracker()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
    '''外部调用'''
    def run(self):
        # 获取并打印所有歌单
        all_playlists = self.getPlayLists()
        tb = prettytable.PrettyTable()
        tb.field_names = ['歌单ID', '歌单名', '歌曲数量', '播放次数', '歌单属性']
        for key, value in all_playlists.items():
            tb.add_row([key]+value)
        self.logging('您创建/收藏的所有歌单如下:')
        print(tb)
        # 根据用户输入获取指定歌单的详情信息
        while True:
            playlist_id = input('请输入想要下载的歌单ID: ')
            if playlist_id in list(all_playlists.keys()):
                song_infos = self.getPlayListSongs(playlist_id, all_playlists[playlist_id][1])
                tb = prettytable.PrettyTable()
                tb.field_names = ['歌曲ID', '歌曲名', '歌手']
                for key, value in song_infos.items():
                    tb.add_row([key]+value[:-1])
                self.logging('您输入的歌单ID为%s, 该歌单的所有歌曲信息如下:' % playlist_id)
                print(tb)
                user_choice = input('是否下载该歌单的所有歌曲(y/n, yes by default): ')
                if (not user_choice) or (user_choice == 'y') or (user_choice == 'yes'):
                    savedir = all_playlists[playlist_id][0]
                    if not os.path.exists(savedir):
                        os.mkdir(savedir)
                    for key, value in song_infos.items():
                        self.downloadSong(key, value[0], value[-1], savedir)
                    self.logging('歌单ID为%s中的所有歌曲下载完成, 保存在 ——> %s' % (playlist_id, savedir))
    '''下载某首歌曲'''
    def downloadSong(self, songid, songname, brs, savedir='.'):
        play_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        self.logging('正在下载 ——> %s' % songname)
        for br in brs:
            data = {
                'ids': [songid],
                'br': br.get('br'),
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
    '''获得某歌单的所有歌曲信息'''
    def getPlayListSongs(self, playlist_id, num_songs):
        detail_url = 'https://music.163.com/weapi/v6/playlist/detail?csrf_token='
        offset = 0
        song_infos = {}
        while True:
            data = {
                'id': playlist_id,
                'offset': offset,
                'total': True,
                'limit': 1000,
                'n': 1000,
                'csrf_token': self.csrf
            }
            response = self.session.post(detail_url+self.csrf, headers=self.headers, data=self.cracker.get(data))
            tracks = response.json()['playlist']['tracks']
            for track in tracks:
                name = track.get('name')
                songid = track.get('id')
                artists = ','.join([i.get('name') for i in track.get('ar')])
                brs = [track.get('h')] + [track.get('m')] + [track.get('l')]
                song_infos[songid] = [name, artists, brs]
            offset += 1
            if len(list(song_infos.keys())) >= num_songs:
                break
        return song_infos
    '''获得所有歌单'''
    def getPlayLists(self):
        playlist_url = 'https://music.163.com/weapi/user/playlist?csrf_token='
        playlists = []
        offset = 0
        while True:
            data = {
                "offset": offset,
                "uid": self.userid,
                "limit": 50,
                "csrf_token": self.csrf
            }
            response = self.session.post(playlist_url+self.csrf, headers=self.headers, data=self.cracker.get(data))
            playlists += response.json()['playlist']
            offset += 1
            if response.json()['more'] == False:
                break
        all_playlists = {}
        for item in playlists:
            name = item.get('name')
            track_count = item.get('trackCount')
            play_count = item.get('playCount')
            play_id = item.get('id')
            if item.get('creator').get('userId') == self.userid:
                attr = '我创建的歌单'
            else:
                attr = '我收藏的歌单'
            all_playlists[str(play_id)] = [name, track_count, play_count, attr]
        return all_playlists
    '''模拟登录'''
    def login(self):
        client = login.Client()
        music163 = client.music163(reload_history=True)
        infos_return, session = music163.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return infos_return, session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')