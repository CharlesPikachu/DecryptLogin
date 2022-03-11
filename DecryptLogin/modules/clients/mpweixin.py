'''
Function:
    微信公众号客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''微信公众号客户端'''
class MpweixinClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(MpweixinClient, self).__init__(website_name='mpweixin', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        token = infos_return['redirect_url'].split('=')[-1]
        url = f'https://mp.weixin.qq.com/cgi-bin/home?action=get_finder_live_info&token={token}&lang=zh_CN&f=json&ajax=1'
        response = session.get(url, headers=headers)
        if 'ok' in response.text:
            return False
        return True