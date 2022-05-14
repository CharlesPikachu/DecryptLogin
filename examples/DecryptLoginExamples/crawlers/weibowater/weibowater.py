'''
Function:
    一个简单的微博水军机器人
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import random
from DecryptLogin import login


'''一个简单的微博水军机器人'''
class WeiboWater():
    def __init__(self, username='charlespikachu', password='微信公众号: Charles的皮卡丘', targetid='6512991534'):
        self.username = username
        self.password = password
        self.targetid = targetid
        self.comments = ['转发微博', '太赞了', '真棒', '挺好的', '宣传一下']
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
    '''运行'''
    def run(self):
        # 模拟登录
        client = login.Client()
        weibo = client.weibo(reload_history=True)
        infos_return, session = weibo.login(self.username, self.password, 'mobile')
        # 获取目标用户最新发表的一条微博
        url = f'https://m.weibo.cn/u/{self.targetid}?uid={self.targetid}&luicode=10000011&lfid=231093_-_selffollowed'
        session.get(url, headers=self.headers)
        containerid = re.findall(r'fid%3D(\d+)%26', str(session.cookies))[0]
        url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={self.targetid}&containerid={containerid}'
        response = session.get(url, headers=self.headers)
        for item in response.json()['data']['tabsInfo']['tabs']:
            if item['tab_type'] == 'weibo': containerid = item['containerid']
        url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={self.targetid}&containerid={containerid}'
        response = session.get(url, headers=self.headers)
        cards = response.json()['data']['cards']
        for card in cards:
            if card['card_type'] == 9:
                self.logging(f'选择的用户微博为 >>>\n{card}')
                break
        selected_card = card
        # 自动点赞
        card_id = selected_card['mblog']['id']
        response = session.get('https://m.weibo.cn/api/config')
        st = response.json()['data']['st']
        flag, response_json = self.starweibo(session, st, card_id)
        if flag:
            self.logging(f'自动点赞ID为{card_id}的微博成功')
        else:
            self.logging(f'自动点赞ID为{card_id}的微博失败, 返回的内容为 >>>\n{response_json}')
        # 自动转发+评论
        flag, response_json = self.repost(session, st, card_id)
        if flag:
            self.logging(f'自动转发+评论ID为{card_id}的微博成功')
        else:
            self.logging(f'自动转发+评论ID为{card_id}的微博失败, 返回的内容为 >>>\n{response_json}')
    '''自动转发+评论'''
    def repost(self, session, st, card_id):
        url = 'https://m.weibo.cn/api/statuses/repost'
        data = {
            'id': card_id,
            'content': random.choice(self.comments),
            'dualPost': 1,
            'mid': card_id,
            'st': st,
        }
        response = session.post(url, data=data)
        if 'ok' in response.json() and str(response.json()['ok']) == '1':
            return True, response.json()
        return False, response.json()
    '''自动点赞'''
    def starweibo(self, session, st, card_id):
        session.headers.update({
            'origin': 'https://m.weibo.cn',
            'referer': f'https://m.weibo.cn/u/{self.targetid}?uid={self.targetid}',
        })
        data = {
            'id': card_id,
            'attitude': 'heart',
            'st': st,
            '_spr': 'screen:1536x864',
        }
        url = 'https://m.weibo.cn/api/attitudes/create'
        response = session.post(url, data=data)
        if 'ok' in response.json() and str(response.json()['ok']) == '1':
            return True, response.json()
        return False, response.json()
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')