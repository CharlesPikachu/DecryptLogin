'''
Function:
    微博客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''微博客户端'''
class WeiboClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(WeiboClient, self).__init__(website_name='weibo', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'http://weibo.com/'
        response = session.get(url)
        if infos_return['nick'] in response.text:
            return False
        return True