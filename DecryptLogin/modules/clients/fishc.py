'''
Function:
    鱼C论坛客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import re
from .baseclient import BaseClient


'''鱼C论坛客户端'''
class FishCClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(FishCClient, self).__init__(website_name='fishc', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://fishc.com.cn/'
        response = session.get(url)
        nickname = re.findall(r'title="访问我的空间">(.*?)</a>', response.text)[0]
        if infos_return['nickname'] == nickname:
            return False
        return True