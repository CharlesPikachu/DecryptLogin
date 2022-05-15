'''
Function:
    微博自动转发抽奖
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import random
from DecryptLogin import login


'''微博自动转发抽奖'''
class WeiboLottery():
    def __init__(self, username='charlespikachu', password='微信公众号: Charles的皮卡丘', time_interval=1800):
        self.username = username
        self.password = password
        self.time_interval = time_interval
        self.comments = ['中奖选我选我选我', '好运锦鲤 捞我吧', '何以解忧，唯有暴富', '何以解忧，唯有中奖']
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
    '''运行'''
    def run(self):
        # 模拟登录
        client = login.Client()
        weibo = client.weibo(reload_history=True)
        infos_return, session = weibo.login(self.username, self.password, 'mobile')
        # 用于存储检查过的微博
        targetid_list = self.getfollows(session)
        repost_weibos_dict = {}
        for targetid in targetid_list:
            repost_weibos_dict[targetid] = []
        # 每隔一段时间遍历一遍目标用户, 把有抽奖信息的微博都转发一遍
        self.logging('初始化完成, 开始自动检测抽奖相关的微博')
        while True:
            for targetid in targetid_list:
                print(f'正在检测用户{targetid}是否发布了新的抽奖微博')
                weibos = self.getweibos(session, targetid)
                for card in weibos:
                    if card['mblog']['id'] in repost_weibos_dict[targetid]: 
                        continue
                    else:
                        repost_weibos_dict[targetid].append(card['mblog']['id'])
                    if '抽奖' in card['mblog']['text']:
                        self.logging(f'检测到一条疑似含有抽奖信息的微博: {card}')
                        # 自动点赞
                        card_id = card['mblog']['id']
                        response = session.get('https://m.weibo.cn/api/config')
                        st = response.json()['data']['st']
                        flag, response_json = self.starweibo(session, st, card_id, targetid)
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
                print(f'检测用户{targetid}是否发布了新的抽奖微博完成')
            time.sleep(self.time_interval)
    '''获得目标用户首页所有微博'''
    def getweibos(self, session, targetid):
        url = f'https://m.weibo.cn/u/{targetid}?uid={targetid}&luicode=10000011&lfid=231093_-_selffollowed'
        session.get(url, headers=self.headers)
        containerid = re.findall(r'fid%3D(\d+)%26', str(session.cookies))[0]
        url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={targetid}&containerid={containerid}'
        response = session.get(url, headers=self.headers)
        for item in response.json()['data']['tabsInfo']['tabs']:
            if item['tab_type'] == 'weibo': containerid = item['containerid']
        url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={targetid}&containerid={containerid}'
        response = session.get(url, headers=self.headers)
        cards, weibos = response.json()['data']['cards'], []
        for card in cards:
            if card['card_type'] == 9:
                weibos.append(card)
        return weibos
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
    def starweibo(self, session, st, card_id, targetid):
        session.headers.update({
            'origin': 'https://m.weibo.cn',
            'referer': f'https://m.weibo.cn/u/{targetid}?uid={targetid}',
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
    '''获得关注的用户列表'''
    def getfollows(self, session):
        page, targetid_list = 0, []
        while True:
            page += 1
            response = session.get('https://m.weibo.cn/api/container/getIndex?containerid=231093_-_selffollowed&page={}'.format(page), headers=self.headers)
            profile_urls = re.findall(r'"profile_url":"(.*?)"', response.text)
            if len(profile_urls) == 0: break
            for profile_url in profile_urls: 
                targetid_list.append(re.findall(r'uid=(.*?)&', profile_url)[0])
        return targetid_list
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')