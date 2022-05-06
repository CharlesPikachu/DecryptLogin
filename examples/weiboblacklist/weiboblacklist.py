'''
Function:
    微博批量拉黑
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import argparse
from tqdm import tqdm
from DecryptLogin import login


'''命令行参数解析'''
def parseArgs():
    parser = argparse.ArgumentParser(description='微博批量拉黑脚本')
    parser.add_argument('--username', dest='username', help='微博登录用的账户名', type=str, required=False)
    parser.add_argument('--password', dest='password', help='微博登录用的密码', type=str, required=False)
    parser.add_argument('--filepath', dest='filepath', help='存储想要批量拉黑的用户的文本文件路径', type=str, required=True)
    args = parser.parse_args()
    return args


'''微博批量拉黑'''
class WeiboBlackList():
    def __init__(self, username, password, blacklist_ids):
        self.infos_return, self.session = self.login(username, password)
        self.blacklist_ids = blacklist_ids
        self.headers = {
            'origin': 'https://weibo.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
    '''运行'''
    def run(self):
        url = 'https://weibo.com/aj/filter/block?ajwvr=6'
        pbar = tqdm(self.blacklist_ids)
        for uid in pbar:
            if not uid: continue
            pbar.set_description(f'正在处理用户{uid}')
            data = {
                'uid': uid,
                'filter_type': '1',
                'status': '1',
                'interact': '1',
                'follow': '1',
            }
            self.headers['referer'] = f'http://weibo.com/u/{uid}'
            response = self.session.post(url, data=data, headers=self.headers)
            if response.json()['code'] != '100000':
                print(f'拉黑用户{uid}失败, 原因为: {response.json()["msg"]}')
    '''模拟登录'''
    def login(self, username, password):
        client = login.Client()
        weibo = client.weibo(reload_history=True)
        session, infos_return = weibo.login(username, password, 'mobile')
        return session, infos_return


'''run'''
if __name__ == '__main__':
    args = parseArgs()
    blacklist_ids = [item.strip() for item in open(args.filepath, 'r').readlines()]
    client = WeiboBlackList(args.username, args.password, blacklist_ids)
    client.run()