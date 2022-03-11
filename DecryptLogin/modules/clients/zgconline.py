'''
Function:
    中关村在线客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import time
from .baseclient import BaseClient


'''中关村在线客户端'''
class ZgconlineClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(ZgconlineClient, self).__init__(website_name='zgconline', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = f'https://my.zol.com.cn/index.php'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        params = {
            'c': 'Ajax_CalendarCheckV4',
            'a': 'InitSign',
            'callback': 'jQuery171013486989978367947_1646973223254',
            '_': str(int(time.time() * 1000)),
        }
        response = session.get(url, headers=headers, params=params)
        if 'signKeep' in response.text:
            return False
        return True