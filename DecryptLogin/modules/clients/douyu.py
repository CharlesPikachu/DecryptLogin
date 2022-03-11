'''
Function:
    斗鱼客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import re
from .baseclient import BaseClient


'''斗鱼客户端'''
class DouyuClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(DouyuClient, self).__init__(website_name='douyu', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://www.douyu.com/member'
        response = session.get(url)
        username = re.findall(r'uname_con clearfix" title="(.*?)"', response.text)[0]
        if infos_return['username'] == username:
            return False
        return True