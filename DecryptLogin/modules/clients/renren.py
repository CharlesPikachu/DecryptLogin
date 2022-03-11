'''
Function:
    人人网客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
import time
import hashlib
from .baseclient import BaseClient


'''人人网客户端'''
class RenRenClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(RenRenClient, self).__init__(website_name='renren', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'https://rrwapi.renren.com/feed/v1/homepage'
        secret_key = infos_return['data']['secretKey']
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'origin': 'http://www.renren.com',
            'referer': 'http://www.renren.com/',
        }
        data = {
            'appKey': 'bcceb522717c2c49f895b561fa913d10',
            'app_ver': '1.0.0',
            'callId': str(int(time.time() * 1000)),
            'count': 20,
            'home_id': infos_return['data']['uid'],
            'product_id': 2080928,
            'sessionKey': infos_return['data']['sessionKey'],
            'uid': int(infos_return['data']['uid']),
        }
        data['sig'] = self.getsign(data, secret_key)
        response = session.post(url, json=data, headers=headers)
        if 'count' in response.json():
            return False
        return True
    '''获得签名'''
    def getsign(self, data, secret_key):
        sign = ''.join(f'{k}={data[k]}' for k in sorted(data.keys()))
        sign += secret_key
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        return sign