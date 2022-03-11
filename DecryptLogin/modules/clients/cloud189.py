'''
Function:
    天翼云盘客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''天翼云盘客户端'''
class Cloud189Client(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(Cloud189Client, self).__init__(website_name='cloud189', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
        url = 'https://cloud.189.cn/api/open/user/getUserInfoForPortal.action?noCache=0.4971582793833025'
        response = session.get(url, headers=headers)
        if '成功' in response.text:
            return False
        return True