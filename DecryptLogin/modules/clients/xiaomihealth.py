'''
Function:
    小米健康客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''小米健康客户端'''
class XiaomiHealthClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(XiaomiHealthClient, self).__init__(website_name='xiaomihealth', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        login_token = infos_return['token_info']['login_token']
        url = 'https://account-cn.huami.com/v1/client/app_tokens'
        headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/20.6.18)'}
        params = {
            'app_name': 'com.xiaomi.hm.health',
            'dn': 'api-user.huami.com%2Capi-mifit.huami.com%2Capp-analytics.huami.com',
            'login_token': login_token,
        }
        response = self.session.get(url, params=params, headers=headers)
        if  response.json().get('token_info', {}).get('app_token', ''):
            return False
        return True