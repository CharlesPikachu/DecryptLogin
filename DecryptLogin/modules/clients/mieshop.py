'''
Function:
    小米商城客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import time
import requests
from .baseclient import BaseClient


'''小米商城客户端'''
class MieShopClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(MieShopClient, self).__init__(website_name='mieshop', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        cookies = requests.utils.dict_from_cookiejar(session.cookies)
        cookies_str = []
        for key in cookies.keys():
            cookies_str.append(f'{key}={cookies[key]}')
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'origin': 'https://www.mi.com',
            'referer': 'https://www.mi.com/',
            'cookie': '; '.join(cookies_str),
        }
        url = f'https://api2.service.order.mi.com/user/userinfo?t={int(time.time())}'
        response = session.get(url, headers=headers)
        if 'success' in response.text:
            return False
        return True