'''
Function:
    QQ音乐客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-17
'''
import time
from .baseclient import BaseClient


'''QQ音乐客户端'''
class QQMusicClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(QQMusicClient, self).__init__(website_name='qqmusic', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        params = {
            '_': str(int(time.time() * 1000)),
            'cv': '4747474',
            'ct': '20',
            'format': 'json',
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '1',
            'uin': infos_return['username'],
            'g_tk_new_20200303': self.gettoken(session.cookies.get('qm_keyst')),
            'g_tk': self.gettoken(session.cookies.get('qm_keyst')),
            'cid': '205360838',
            'userid': '0',
            'reqfrom': '1',
            'reqtype': '0',
        } 
        headers = {
            'origin': 'https://y.qq.com',
            'referer': 'https://y.qq.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
        url = 'https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg'
        response = session.get(url, params=params, headers=headers)
        if response.json()['code'] == 0:
            return False
        return True
    '''获得token'''
    def gettoken(self, skey):
        e = 5381
        for c in skey:
            e += (e << 5) + ord(c)
        return 0x7fffffff & e