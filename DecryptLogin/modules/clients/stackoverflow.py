'''
Function:
    Stackoverflow客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import re
from .baseclient import BaseClient


'''Stackoverflow客户端'''
class StackoverflowClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(StackoverflowClient, self).__init__(website_name='stackoverflow', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://stackoverflow.com/'
        response = session.get(url)
        profile_url = 'https://stackoverflow.com' + re.findall(r'<a href="(.+)" class="my-profile', response.text)[0]
        if infos_return['profile_url'] == profile_url:
            return False
        return True