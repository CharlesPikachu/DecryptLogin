'''
Function:
    百度客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-05-09
'''
from .baseclient import BaseClient


'''百度客户端'''
class BaiduClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(BaiduClient, self).__init__(website_name='baidu', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://tieba.baidu.com/f/user/json_userinfo'
        response = session.get(url)
        username = response.json()['data']['user_name_show']
        if username == infos_return['username']:
            return False
        return True