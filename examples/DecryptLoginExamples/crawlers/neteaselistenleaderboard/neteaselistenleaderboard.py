'''
Function:
    网易云个人听歌排行榜
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import prettytable
from DecryptLogin import login
from DecryptLogin.modules.core.music163 import Cracker


'''网易云个人听歌排行榜爬取'''
class NeteaseListenLeaderboard():
    def __init__(self, username='charlespikachu'):
        self.username = username
        self.session = self.login()
        self.csrf = re.findall('__csrf=(.*?) for', str(self.session.cookies))[0]
        self.cracker = Cracker()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
    '''外部调用'''
    def run(self):
        while True:
            userid = input('网易云个人听歌排行榜爬取, 请输入目标用户id(例如:268390054) ——> ')
            leader_board = self.getLeaderboard(userid)
            self.logging('用户%s的最近一周听歌榜:' % userid)
            tb = prettytable.PrettyTable()
            tb.field_names = ['歌曲ID', '歌单名', '播放次数']
            for each in leader_board.get('weekData'):
                tb.add_row(each)
            print(tb)
            self.logging('用户%s的所有时间听歌榜:' % userid)
            tb = prettytable.PrettyTable()
            tb.field_names = ['歌曲ID', '歌单名', '播放次数']
            for each in leader_board.get('allData'):
                tb.add_row(each)
            print(tb)
    '''获得某用户的听歌排行榜'''
    def getLeaderboard(self, uid):
        url = 'https://music.163.com/weapi/v1/play/record?csrf_token=' + self.csrf
        data = {
            'type': '-1',
            'uid': uid,
            'limit': '1000',
            'offset': '0',
            'total': 'true',
            'csrf_token': self.csrf
        }
        response = self.session.post(url, headers=self.headers, data=self.cracker.get(data))
        response_json = response.json()
        leader_board = {'weekData': [], 'allData': []}
        if response_json['code'] == 200:
            all_data = response_json.get('allData')
            for item in all_data:
                songname = item.get('song').get('name')
                songid = item.get('song').get('id')
                play_count = item.get('playCount')
                leader_board['allData'].append([songid, songname, play_count])
            week_data = response_json.get('weekData')
            for item in week_data:
                songname = item.get('song').get('name')
                songid = item.get('song').get('id')
                play_count = item.get('playCount')
                leader_board['weekData'].append([songid, songname, play_count])
        else:
            raise RuntimeError('Fail to get leaderboard for %s' % uid)
        return leader_board
    '''模拟登录'''
    def login(self):
        client = login.Client()
        music163 = client.music163(reload_history=True)
        infos_return, session = music163.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')