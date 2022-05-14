'''
Function:
    微博监控
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from DecryptLogin import login


'''微博监控'''
class WeiboMonitor():
    def __init__(self, username, password, time_interval=30):
        _, self.session = self.login(username, password)
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'm.weibo.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.api_url = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value={}&containerid={}'
        self.time_interval = time_interval
    '''开始监控'''
    def run(self):
        followed = self.getFollowed()
        self.logging('请选择一位您关注列表中的用户进行监控:')
        self.logging('-' * 40)
        for idx, each in enumerate(sorted(followed.keys())):
            self.logging('[%d]. %s' % (idx+1, each))
        self.logging('-' * 40)
        while True:
            user_choice = input('请选择您想要监控的用户编号(例如1):')
            try:
                profile_url = followed[sorted(followed.keys())[int(user_choice)-1]]
                user_id = re.findall(r'uid=(\d+)&', profile_url)[0]
                break
            except:
                self.logging('您的输入有误, 请重新输入.', 'Warning')
        self.monitor(user_id, profile_url)
    '''监控用户主页'''
    def monitor(self, user_id, profile_url):
        user_name, containerid = self.getContainerid(user_id, profile_url)
        response = self.session.get(self.api_url.format(user_id, user_id, containerid))
        weibo_ids = []
        cards = response.json()['data']['cards']
        for card in cards:
            if card['card_type'] == 9:
                weibo_ids.append(str(card['mblog']['id']))
        while True:
            weibo_ids = self.checkUpdate(user_id, profile_url, weibo_ids)
            time.sleep(self.time_interval)
    '''检查用户是否有新的微博'''
    def checkUpdate(self, user_id, profile_url, weibo_ids):
        user_name, containerid = self.getContainerid(user_id, profile_url)
        response = self.session.get(self.api_url.format(user_id, user_id, containerid))
        cards = response.json()['data']['cards']
        flag = False
        for card in cards:
            if card['card_type'] == 9:
                if str(card['mblog']['id']) not in weibo_ids:
                    flag = True
                    weibo_ids.append(str(card['mblog']['id']))
                    self.logging(f'用户{user_name}发布了新微博')
                    pics = []
                    if card['mblog'].get('pics'):
                        for i in card['mblog']['pics']: pics.append(i['url'])
                    pics = '||'.join(pics)
                    self.logging(card)
        if not flag: self.logging(f'用户{user_name}未发布新微博')
        return weibo_ids
    '''获取containerid'''
    def getContainerid(self, user_id, profile_url):
        self.session.get(profile_url)
        containerid = re.findall(r'fid%3D(\d+)%26', str(self.session.cookies))[0]
        response = self.session.get(self.api_url.format(user_id, user_id, containerid))
        user_name = self.decode(re.findall(r'"screen_name":"(.*?)"', response.text)[0])
        for i in response.json()['data']['tabsInfo']['tabs']:
            if i['tab_type'] == 'weibo':
                containerid = i['containerid']
        return user_name, containerid
    '''获取关注列表'''
    def getFollowed(self):
        data = {}
        page = 0
        while True:
            page += 1
            response = self.session.get('https://m.weibo.cn/api/container/getIndex?containerid=231093_-_selffollowed&page={}'.format(page), headers=self.headers)
            profile_urls = re.findall(r'"profile_url":"(.*?)"', response.text)
            screen_names = re.findall(r'"screen_name":"(.*?)"', response.text)
            if len(profile_urls) == 0:
                break
            for screen_name, profile_url in zip(screen_names, profile_urls):
                data[self.decode(screen_name)] = profile_url.replace('\\', '')
        return data
    '''解码'''
    def decode(self, content):
        return content.encode('latin-1').decode('unicode_escape')
    '''模拟登录'''
    def login(self, username, password):
        client = login.Client()
        weibo = client.weibo(reload_history=True)
        infos_return, session = weibo.login(username, password, 'mobile')
        return infos_return, session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')