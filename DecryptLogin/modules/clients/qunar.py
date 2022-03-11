'''
Function:
    去哪儿旅行客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''去哪儿旅行客户端'''
class QunarClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(QunarClient, self).__init__(website_name='qunar', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://user.qunar.com/webApi/getPwdType.jsp'
        response = session.post(url)
        if 'success' in response.text:
            return False
        return True