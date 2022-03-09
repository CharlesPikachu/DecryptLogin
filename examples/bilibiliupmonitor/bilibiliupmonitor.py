'''
Function:
    B站UP主监控
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import pickle
import argparse
from DecryptLogin import login


'''命令行参数解析'''
def parseArgs():
    parser = argparse.ArgumentParser(description='B站UP主监控')
    parser.add_argument('--ids', dest='ids', help='监控的UP主ID, 例如"406756145,406756146"', type=str, required=False, default='406756145')
    parser.add_argument('--key', dest='key', help='Server酱的Key', type=str, default=None)
    args = parser.parse_args()
    return args


'''B站UP主监控'''
class BilibiliUPMonitor():
    def __init__(self, up_ids=['406756145'], time_interval=1800, server_key=None, **kwargs):
        self.up_ids = up_ids
        self.time_interval = time_interval
        self.server_key = server_key
        if os.path.exists('session.pkl'):
            self.infos_return, self.session = {}, pickle.load(open('session.pkl', 'rb'))
        else:
            self.infos_return, self.session = self.login()
            pickle.dump(self.session, open('session.pkl', 'wb'))
    '''运行'''
    def run(self):
        # 批量关注
        ups_recorder = {}
        for up_id in self.up_ids:
            code, message = self.follow(up_id)
            ups_recorder[up_id] = self.getuserinfo(up_id)
            if code == 0:
                self.logging(f'关注UP主{ups_recorder[up_id]["username"]}成功, 正在进行监控...')
            else:
                self.logging(f'关注UP主{ups_recorder[up_id]["username"]}失败, 原因为{message}...')
        # 获得UP主当前的视频信息
        for up_id in self.up_ids:
            ups_recorder[up_id]['vids'] = self.getupvids(up_id)
        # 自动监控
        while True:
            # --sleep一段时间再检查
            time.sleep(self.time_interval)
            # --检查更新
            for up_id in self.up_ids:
                self.logging(f'正在检查UP主{ups_recorder[up_id]["username"]}是否更新了视频...')
                vids = self.getupvids(up_id)
                ups_recorder[up_id]['updated_vids'] = []
                for vid in vids:
                    if vid in ups_recorder[up_id]['vids']: continue
                    ups_recorder[up_id]['updated_vids'].append(vid)
                    ups_recorder[up_id]['vids'].append(vid)
            # --发送提示并下载
            for up_id in self.up_ids:
                if len(ups_recorder[up_id]['updated_vids']) > 0:
                    msg = f'你关注的UP主{ups_recorder[up_id]["username"]}更新啦...'
                    self.pushwechat(msg)
                    self.logging(msg)
                    for vid in ups_recorder[up_id]['updated_vids']:
                        os.system(f'videodl -i {vid} -s {ups_recorder[up_id]["username"]}')
                else:
                    msg = f'你关注的UP主{ups_recorder[up_id]["username"]}暂时没有更新...'
                    self.logging(msg)
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')
    '''获得用户信息'''
    def getuserinfo(self, up_id):
        params = {'mid': up_id, 'jsonp': 'jsonp'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        response = self.session.get('https://api.bilibili.com/x/space/acc/info', params=params, headers=headers)
        response_json = response.json()
        user_info = {
            'username': response_json['data']['name'],
            'gender': response_json['data']['sex'],
            'sign': response_json['data']['sign'],
            'level': response_json['data']['level'],
            'birthday': response_json['data']['birthday']
        }
        return user_info
    '''获得UP主首页所有视频信息'''
    def getupvids(self, up_id):
        up_vids, aids = [], []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        params = {'keyword': '', 'mid': up_id, 'ps': 30, 'tid': 0, 'pn': 1, 'order': 'pubdate'}
        response = self.session.get('https://api.bilibili.com/x/space/arc/search', headers=headers, params=params)
        response_json = response.json()
        for item in response_json['data']['list']['vlist']:
            aids.append(item['aid'])
        for aid in aids:
            params = {'aid': aid}
            response = self.session.get('https://api.bilibili.com/x/web-interface/view', headers=headers, params=params)
            response_json = response.json()
            up_vids.append('https://www.bilibili.com/video/' + response_json['data']['bvid'])
        return up_vids
    '''发送Server酱提示'''
    def pushwechat(self, desp='你关注的UP主更新啦'):
        if self.server_key is None: return
        server_url = f'https://sc.ftqq.com/{self.server_key}.send'
        params = {
            'text': 'UP主更新提示',
            'desp': desp,
        }
        response = requests.get(server_url, params=params)
        return 
    '''关注某个UP主'''
    def follow(self, up_id):
        url = 'https://api.bilibili.com/x/relation/modify'
        data = {
            'fid': up_id,
            'act': 1,
            're_src': 11,
            'jsonp': 'jsonp',
            'csrf': self.session.cookies.get_dict(domain='.bilibili.com').get('bili_jct', ''),
        }
        headers = {
            'Host': 'api.bilibili.com',
            'Origin': 'https://space.bilibili.com',
            'Referer': f'https://space.bilibili.com/{up_id}/',
        }
        response = self.session.post(url, data=data, headers=headers)
        response_json = response.json()
        return response_json['code'], response_json.get('message', '')
    '''模拟登录'''
    def login(self):
        lg = login.Login()
        infos_return, session = lg.bilibili(mode='scanqr')
        return infos_return, session


'''run'''
if __name__ == '__main__':
    args = parseArgs()
    up_ids = [id_.strip() for id_ in args.ids.split(',')]
    client = BilibiliUPMonitor(up_ids=up_ids, server_key=args.key)
    client.run()