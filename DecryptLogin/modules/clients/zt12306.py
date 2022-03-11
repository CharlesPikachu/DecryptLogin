'''
Function:
    中国铁路12306客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''中国铁路12306客户端'''
class Zt12306Client(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(Zt12306Client, self).__init__(website_name='zt12306', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://kyfw.12306.cn/otn/index/initMy12306Api'
        response = session.post(url)
        if response.json()['status'] and response.json()['httpstatus'] == 200:
            return False
        return True