'''
Function:
    CodaLab客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''CodaLab客户端'''
class CodaLabClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(CodaLabClient, self).__init__(website_name='codalab', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://competitions.codalab.org/'
        response = session.get(url)
        if infos_return['username'] in response.text:
            return False
        return True