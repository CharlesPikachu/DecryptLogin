'''
Function:
    坚果云客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import time
from .baseclient import BaseClient


'''坚果云客户端'''
class JianguoyunClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(JianguoyunClient, self).__init__(website_name='jianguoyun', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = f'https://www.jianguoyun.com/d/ajax/userop/getUserInfo?start=1&_={int(time.time() * 1000)}'
        response = session.get(url)
        if response.json()['accountState'] == 1:
            return False
        return True