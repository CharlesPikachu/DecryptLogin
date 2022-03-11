'''
Function:
    咪咕客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import requests
from .baseclient import BaseClient


'''咪咕客户端'''
class MiguClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(MiguClient, self).__init__(website_name='migu', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        cookies = requests.utils.dict_from_cookiejar(session.cookies)
        cookies_str = []
        for key in cookies.keys():
            cookies_str.append(f'{key}={cookies[key]}')
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'referer': 'https://music.migu.cn/v3/my',
            'cookie': '; '.join(cookies_str),
        }
        url = 'https://music.migu.cn/v3/api/my/listen/listend?page=1'
        response = session.get(url, headers=headers)
        if '成功' in response.text:
            return False
        return True