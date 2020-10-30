'''
Function:
    网易云个人听歌排行榜
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import argparse
import prettytable
from DecryptLogin import login
from DecryptLogin.core.music163 import Cracker


'''命令行参数解析'''
def parseArgs():
	parser = argparse.ArgumentParser(description='爬取目标用户的网易云听歌排行榜')
	parser.add_argument('--username', dest='username', help='用户名', type=str, required=True)
	parser.add_argument('--password', dest='password', help='密码', type=str, required=True)
	return parser.parse_args()


'''网易云个人听歌排行榜爬取'''
class NeteaseListenLeaderboard():
    def __init__(self, username, password, **kwargs):
        _, self.session = login.Login().music163(username, password)
        self.csrf = re.findall('__csrf=(.*?) for', str(self.session.cookies))[0]
        self.cracker = Cracker()
        self.headers = {
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
					}
    def run(self):
        while True:
            userid = input('网易云个人听歌排行榜爬取, 请输入目标用户id(例如:268390054) ——> ')
            leader_board = self.getLeaderboard(userid)
            print('用户%s的最近一周听歌榜:' % userid)
            tb = prettytable.PrettyTable()
            tb.field_names = ['歌曲ID', '歌单名', '播放次数']
            for each in leader_board.get('weekData'):
                tb.add_row(each)
            print(tb)
            print('用户%s的所有时间听歌榜:' % userid)
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
        res = self.session.post(url, headers=self.headers, data=self.cracker.get(data))
        res_json = res.json()
        leader_board = {'weekData': [], 'allData': []}
        if res_json['code'] == 200:
            all_data = res_json.get('allData')
            for item in all_data:
                songname = item.get('song').get('name')
                songid = item.get('song').get('id')
                play_count = item.get('playCount')
                leader_board['allData'].append([songid, songname, play_count])
            week_data = res_json.get('weekData')
            for item in week_data:
                songname = item.get('song').get('name')
                songid = item.get('song').get('id')
                play_count = item.get('playCount')
                leader_board['weekData'].append([songid, songname, play_count])
        else:
            raise RuntimeError('Fail to get leaderboard for %s...' % uid)
        return leader_board


'''run'''
if __name__ == '__main__':
    args = parseArgs()
    handle = NeteaseListenLeaderboard(args.username, args.password)
    handle.run()