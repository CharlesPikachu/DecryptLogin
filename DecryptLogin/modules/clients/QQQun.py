'''
Function:
    QQ群客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''QQ群客户端'''
class QQQunClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(QQQunClient, self).__init__(website_name='QQQun', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        skey = infos_return['cookies']['skey']
        url = f'https://qun.qq.com/cgi-bin/qunwelcome/myinfo?callback=?&bkn={self.skey2bkn(skey)}'
        response = session.get(url, headers=headers)
        if response.json()['retcode'] == 0 and response.json()['cgicode'] == 0:
            return False
        return True
    '''根据skey参数得到bkn参数'''
    def skey2bkn(self, skey):
        bkn = 5381
        for c in skey:
            bkn += (bkn << 5) + ord(c)
        return 2147483647 & bkn