'''
Function:
    B站监控关注的UP主并自动转发抽奖
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import random
from tqdm import tqdm
from DecryptLogin import login


'''B站监控关注的UP主并自动转发抽奖'''
class BiliBiliLottery():
    def __init__(self, username='charlespikachu', time_interval=1800):
        self.username = username
        self.time_interval = time_interval
        self.comments = ['日常当分母', '就想简简单单中个奖QAQ', '啊啊啊啊啊, 让我中一次吧 T_T', '天选之子']
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
    '''运行'''
    def run(self):
        # 模拟登录
        client = login.Client()
        bili = client.bilibili(reload_history=True)
        infos_return, session = bili.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        # 获得关注列表
        self.logging('正在获取您的关注列表')
        followings_ids = self.getfollowings(session, infos_return)
        # 获得UP主当前的动态
        self.logging('正在获取您的关注列表里的UP主的所有动态')
        followings_infos = {}
        for userid in followings_ids:
            followings_infos[userid] = self.getupdates(infos_return, userid, session)
        # 监控新的动态
        self.logging('开始监控是否有新的抽奖信息发布')
        while True:
            time.sleep(self.time_interval)
            self.logging('开始检测是否有新的抽奖信息发布')
            for userid in tqdm(followings_ids):
                updates_old = followings_infos.pop(userid)
                updates_latest = self.getupdates(infos_return, userid, session)
                for dynamic_id in updates_latest.keys():
                    if dynamic_id not in updates_old:
                        desp = updates_latest[dynamic_id]
                        if '#互动抽取#' in desp or '互动抽奖' in desp:
                            result = self.forwardupdate(session, infos_return, dynamic_id)
                            self.logging(f'检测到有新的抽奖信息发布, 已经尝试转发, 返回的结果为{result}')
                followings_infos[userid] = updates_latest
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')
    '''转发动态'''
    def forwardupdate(self, session, infos_return, dynamic_id):
        url = 'http://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost'
        data = {
            'uid': infos_return['data']['mid'],
            'dynamic_id': dynamic_id,
            'content' : random.choice(self.comments),
            'ctrl': '[{"data":"5581898","location":2,"length":4,"type":1},{"data":"10462362","location":7,"length":5,"type":1},{"data":"1577804","location":13,"length":4,"type":1}]',
            'csrf_token': session.cookies.get('bili_jct')
        }
        response = session.post(url, data=data, headers=self.headers)
        return response.json()
    '''获得UP主的动态'''
    def getupdates(self, infos_return, host_uid, session):
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid={infos_return["data"]["mid"]}&host_uid={host_uid}&offset_dynamic_id=0&need_top=1&platform=web'
        response = session.get(url, headers=self.headers)
        response_json, updates = response.json(), {}
        for card in response_json['data']['cards']:
            dynamic_id = card['desc']['dynamic_id']
            try:
                desp = re.findall(r'"description":"(.*?)"', card['card'])[0]
            except:
                desp = ''
            updates[dynamic_id] = desp
        return updates
    '''获得关注列表'''
    def getfollowings(self, session, infos_return):
        url = 'https://api.bilibili.com/x/relation/followings'
        params = {
            'vmid': infos_return['data']['mid'],
            'pn': '1',
            'ps': '20',
            'order': 'desc',
            'order_type': 'attention',
            'jsonp': 'jsonp',
        }
        response = session.get(url, params=params, headers=self.headers)
        total = response.json()['data']['total']
        followings_ids, page = [], 1
        while True:
            for item in response.json()['data']['list']:
                followings_ids.append(item['mid'])
            if len(followings_ids) >= total: break
            page += 1
            params['pn'] = str(page)
            response = session.get(url, params=params, headers=self.headers)
        return followings_ids