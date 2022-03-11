'''
Function:
    搜狐客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import time
import hashlib
from .baseclient import BaseClient


'''搜狐客户端'''
class SohuClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(SohuClient, self).__init__(website_name='sohu', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://uis.mp.sohu.com/apiv2/user/auth/wapLogin'
        ts = str(int(time.time() * 1000))
        headers = {
            'appkey': '4003',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'sig': self.getsign(ts),
            'ts': ts,
            'origin': 'https://www.sohu.com',
        }
        response = session.post(url, headers=headers)
        if response.json()['code'] == 200:
            return False
        return True
    '''获得sig值'''
    def getsign(self, ts):
        sig = f'appkey=4003&ts={ts}395e615ffa1fdc85dd072387d6b75ba4'
        return hashlib.md5(sig.encode('utf-8')).hexdigest()