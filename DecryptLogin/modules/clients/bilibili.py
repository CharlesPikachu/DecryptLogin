'''
Function:
    B站客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''B站客户端'''
class BiliBiliClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(BiliBiliClient, self).__init__(website_name='bilibili', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session):
        url = 'https://api.bilibili.com/x/web-interface/nav/stat'
        response = session.get(url)
        response_json = response.json()
        if str(response_json['code']) == '0' and str(response_json['message']) == '0':
            return False
        return True