'''
Function:
    网易云音乐刷歌曲播放量
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import json
import time
import requests
import prettytable
from DecryptLogin import login
from DecryptLogin.modules.core.music163 import Cracker


'''网易云音乐歌曲刷歌曲播放量'''
class NeteaseClickPlaylist():
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
            playlist_id = input('请输入想要刷的歌单ID: ')
            if playlist_id not in all_playlists:
                self.logging('输入的歌单ID有误', 'Error')
                continue
            num_times = input('请输入循环播放次数: ')
            try:
                num_times = int(num_times)
            except:
                self.logging('循环播放次数必须为整数', 'Error')
                continue
            for idx in range(num_times):
                self.logging('正在循环播放第%d/%d次' % (idx+1, num_times))
                self.clickplaylist(playlist_id, all_playlists)
    '''刷某个歌单的播放量'''
    def clickplaylist(self, playlist_id, all_playlists):
        url = 'http://music.163.com/weapi/feedback/weblog'
        song_infos = self.getPlayListSongs(playlist_id, all_playlists[playlist_id][1])
        for songid in list(song_infos.keys()):
            data = {
                'logs': json.dumps([{
                    'action': 'play',
                    'json': {
                        'download': 0,
                        'end': 'playend',
                        'id': songid,
                        'sourceId': '',
                        'time': '240',
                        'type': 'song',
                        'wifi': '0'
                    }
                }])
            }
            response = self.session.post(url, headers=self.headers, data=self.cracker.get(data))
            self.logging(f"{song_infos[songid]}")
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