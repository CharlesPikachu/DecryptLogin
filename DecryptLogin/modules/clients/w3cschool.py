'''
Function:
    W3CSchool客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import requests
from .baseclient import BaseClient


'''W3CSchool客户端'''
class W3CSchoolClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(W3CSchoolClient, self).__init__(website_name='w3cschool', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://www.w3cschool.cn/index/checkHeader'
        cookies = requests.utils.dict_from_cookiejar(session.cookies)
        cookies_str = []
        for key in ['PHPSESSID', 'ypre_saltkey', 'ypre_auth', 'ypre_sauth', 'ypre_uid']:
            cookies_str.append(f'{key}={cookies[key]}')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Host': 'www.w3cschool.cn',
            'Origin': 'https://www.w3cschool.cn',
            'Referer': 'https://www.w3cschool.cn/my',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': '; '.join(cookies_str),
        }
        data = {
            'headerType': '0',
            '_hash': session.cookies.get('ypre_saltkey'),
        }
        response = session.post(url, headers=headers, data=data)
        if response.json()['statusCode'] == 200:
            return False
        return True