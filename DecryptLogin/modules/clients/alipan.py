'''
Function:
    阿里云客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-07-19
'''
import re
import requests
from .baseclient import BaseClient


'''阿里云客户端'''
class AlipanClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(AlipanClient, self).__init__(website_name='alipan', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://api.aliyundrive.com/token/refresh'
        response = requests.post(url, json={'refresh_token': infos_return['refresh_token']})
        if response.status_code == 200:
            return False
        return True