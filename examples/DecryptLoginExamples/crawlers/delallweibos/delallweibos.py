'''
Function:
    批量删除自己所有的微博
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import random
from DecryptLogin import login


'''删除用户的所有微博'''
class DelAllWeibos():
    def __init__(self, username, password):
        infos_return, self.session = self.login(username, password)
        self.user_id = re.findall(r'uid%3D(\d+)', self.session.cookies.get('ALC'))[0]
        self.api_url = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=231093_-_selffollowed&type=uid&value={}&containerid={}'
        self.format_profile_url = 'https://m.weibo.cn/u/{}?uid={}&luicode=10000011&lfid=231093_-_selffollowed'
    '''外部调用'''
    def run(self):
        user_input = input('仔细考虑一下, 你真的想删除自己所有的微博嘛?(yes/no):')
        if not (user_input.lower() == 'yes' or user_input.lower() == 'y'):
            return
        url = 'https://weibo.com/aj/mblog/del?ajwvr=6'
        headers = {
            'Referer': f'http://weibo.com/{self.user_id}/profile?rightmod=1&wvr=6&mod=personnumber&is_all=1'
        }
        del_count = 0
        total_count = 0
        while True:
            weibo_mids = self.getweibolist()
            if not weibo_mids:
                break
            for mid in weibo_mids:
                total_count += 1
                self.logging('正在处理第%s条微博, 已成功删除%s条微博' % (total_count, del_count))
                response = self.session.post(url, data={'mid': mid}, headers=headers)
                if response.json()['code'] == '100000':
                    del_count += 1
                time.sleep(random.randrange(1, 3)+random.random())
            time.sleep(random.randrange(3, 6)+random.random())
        self.logging('程序运行完毕, 共检测到您的账户一共有%s条微博, 其中%s条已被成功删除' % (total_count, del_count))
    '''获得用户首页的微博列表'''
    def getweibolist(self):
        profile_url = self.format_profile_url.format(self.user_id, self.user_id)
        user_name, containerid = self.getContainerid(self.user_id, profile_url)
        response = self.session.get(self.api_url.format(self.user_id, self.user_id, containerid))
        cards = response.json()['data']['cards']
        weibo_ids = []
        for card in cards:
            if card['card_type'] == 9:
                weibo_ids.append(str(card['mblog']['id']))
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