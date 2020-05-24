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
import argparse
from DecryptLogin import login


'''命令行参数解析'''
def parseArgs():
    parser = argparse.ArgumentParser(description='批量删除自己所有的微博')
    parser.add_argument('--username', dest='username', help='用户名', type=str, required=True)
    parser.add_argument('--password', dest='password', help='密码', type=str, required=True)
    args = parser.parse_args()
    return args


'''删除用户的所有微博'''
class delallweibos():
    def __init__(self, username, password, **kwargs):
        infos_return, self.session = delallweibos.login(username, password)
        self.user_id = infos_return.get('uid')
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
            weibo_mids = self.__getweibolist()
            if not weibo_mids:
                break
            for mid in weibo_mids:
                total_count += 1
                print('[INFO]: 正在处理第%s条微博, 已成功删除%s条微博...' % (total_count, del_count))
                response = self.session.post(url, data={'mid': mid}, headers=headers)
                if response.json()['code'] == '100000':
                    del_count += 1
                time.sleep(random.randrange(1, 3)+random.random())
            time.sleep(random.randrange(3, 6)+random.random())
        print('[INFO]: 程序运行完毕, 共检测到您的账户一共有%s条微博, 其中%s条已被成功删除...' % (total_count, del_count))
    '''获得用户首页的微博列表'''
    def __getweibolist(self):
        url = 'https://weibo.com/p/aj/v6/mblog/mbloglist'
        params = {
                    'ajwvr': '6',
                    'domain': '100505',
                    'is_search': '0',
                    'visible': '0',
                    'is_all': '1',
                    'is_tag': '0',
                    'profile_ftype': '1',
                    'page': '1',
                    'pagebar': '1',
                    'pl_name': 'Pl_Official_MyProfileFeed__19',
                    'id': f'100505{self.user_id}',
                    'script_uri': f'/{self.user_id}/profile',
                    'feed_type': '0',
                    'pre_page': '5',
                    'domain_op': '100505',
                    '__rnd': str(time.time()*1000)[:13]
                }
        response = self.session.get(url, params=params)
        data = response.json()['data']
        weibo_mids = re.findall(r'\s+mid="(\d+)"\s+', data)
        return weibo_mids
    '''微博模拟登录'''
    @staticmethod
    def login(username, password):
        lg = login.Login()
        infos_return, session = lg.weibo(username, password, 'pc')
        return infos_return, session


'''run'''
if __name__ == '__main__':
    args = parseArgs()
    client = delallweibos(args.username, args.password)
    client.run()