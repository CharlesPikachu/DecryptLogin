'''
Function:
    京东客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import time
from .baseclient import BaseClient


'''京东客户端'''
class JingdongClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(JingdongClient, self).__init__(website_name='jingdong', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        url = f'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action?callback=jQuery1656884&_={int(time.time() * 1000)}'
        response = session.get(url, headers=headers)
        if infos_return['nickname'] in response.text:
            return False
        return True