'''
Function:
    今日头条客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''今日头条客户端'''
class ToutiaoClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(ToutiaoClient, self).__init__(website_name='toutiao', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://www.toutiao.com/tt-anti-token'
        response = session.get(url)
        if response.json()['message'] == 'Success':
            return False
        return True