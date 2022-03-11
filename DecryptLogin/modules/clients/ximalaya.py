'''
Function:
    喜马拉雅客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''喜马拉雅客户端'''
class XimalayaClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(XimalayaClient, self).__init__(website_name='ximalaya', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
        url = 'https://www.ximalaya.com/revision/main/getCurrentUser'
        response = session.get(url, headers=headers)
        if response.json()['ret'] == 200:
            return False
        return True