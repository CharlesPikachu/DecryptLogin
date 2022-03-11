'''
Function:
    凤凰网客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''凤凰网客户端'''
class IfengClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(IfengClient, self).__init__(website_name='ifeng', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Host': 'user.ifeng.com',
            'Referer': 'https://user.ifeng.com/my/info'
        }
        url = 'https://user.ifeng.com/api/v1/get/userinfobytoken?platform=w&systemid=1'
        response = session.get(url, headers=headers)
        if response.json()['user_status'] == 0:
            return False
        return True