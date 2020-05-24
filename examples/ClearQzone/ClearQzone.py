'''
Function:
    批量删除QQ空间说说
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import json
import time
import random
import argparse
from DecryptLogin import login


'''命令行参数解析'''
def parseArgs():
    parser = argparse.ArgumentParser(description='批量删除QQ空间说说')
    parser.add_argument('--manual', dest='manual', help='每条说说删除前是否需要手动确认', action='store_true')
    args = parser.parse_args()
    return args


'''批量删除说说'''
class ClearQzone():
    def __init__(self, is_manual, **kwargs):
        self.is_manual = is_manual
        infos_return, self.session = ClearQzone.login()
        self.uin = infos_return.get('username')
        p_skey = re.findall(r'p_skey=(.*?) ', str(self.session.cookies))[0]
        self.g_tk = self.__calcGtk(p_skey)
        self.qzonetoken = '12a2df7fc3ce126e67c62b0577cdea5133e79e77f46ae920b2a8b822ac867e54416698be9ee883f09e'
    '''外部调用'''
    def run(self):
        url = 'https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_delete_v6?'
        del_count = 0
        total_count = 0
        while True:
            all_twitters = self.__getAllTwitters()
            if not all_twitters:
                break
            for key, value in all_twitters.items():
                total_count += 1
                print('[INFO]: 正在处理第%s条说说, 已成功删除%s条说说...' % (total_count, del_count))
                if self.is_manual:
                    print('说说时间: %s, 说说内容: %s...' % (str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value[0]))), value[1]))
                    user_input = input('是否需要删除该条说说(yes/no): ')
                    if user_input.lower() == 'n' or user_input.lower() == 'no':
                        continue
                data = {
                            'hostuin': self.uin,
                            'tid': key,
                            't1_source': '1',
                            'code_version': '1',
                            'format': 'fs',
                            'qzreferrer': f'https://user.qzone.qq.com/{self.uin}/infocenter'
                        }
                params = {
                            'qzonetoken': self.qzonetoken,
                            'g_tk': self.g_tk
                        }
                try:
                    response = self.session.post(url, data=data, params=params)
                    del_count += 1
                    time.sleep(random.randrange(1, 3)+random.random())
                except:
                    pass
            time.sleep(random.randrange(3, 6)+random.random())
        print('[INFO]: 程序运行完毕, 共检测到您的账户一共有%s条说说, 其中%s条已被成功删除...' % (total_count, del_count))
    '''获得首页的说说数据'''
    def __getAllTwitters(self):
        url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        params = {
                    'uin': self.uin,
                    'ftype': '0',
                    'sort': '0',
                    'pos': '0',
                    'num': '20',
                    'replynum': '100',
                    'g_tk': self.g_tk,
                    'callback': '_preloadCallback',
                    'code_version': '1',
                    'format': 'jsonp',
                    'need_private_comment': '1',
                    'qzonetoken': self.qzonetoken
                }
        response = self.session.get(url, params=params)
        response_json = response.content.decode('utf-8').replace('_preloadCallback(', '')[:-2]
        response_json = json.loads(response_json)
        msglist = response_json['msglist']
        if msglist is None:
            msglist = []
        all_twitters = {}
        for item in msglist:
            tid = item['tid']
            created_time = item['created_time']
            content = item['content']
            all_twitters[tid] = [created_time, content]
        return all_twitters
    '''计算g_tk'''
    def __calcGtk(self, string):
        e = 5381
        for c in string:
            e += (e << 5) + ord(c)
        return 2147483647 & e
    '''QQ空间模拟登录'''
    @staticmethod
    def login():
        lg = login.Login()
        infos_return, session = lg.QQZone()
        return infos_return, session


'''run'''
if __name__ == '__main__':
    args = parseArgs()
    client = ClearQzone(args.manual)
    client.run()