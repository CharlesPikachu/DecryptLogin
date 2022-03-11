'''
Function:
    QQ空间客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''QQ空间客户端'''
class QQZoneClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(QQZoneClient, self).__init__(website_name='QQZone', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        url = 'https://user.qzone.qq.com/' + infos_return['username']
        response = session.get(url, headers=headers)
        if 'ownerProfileSummary' in response.text:
            return False
        return True