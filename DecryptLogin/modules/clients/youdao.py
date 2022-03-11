'''
Function:
    有道客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-11
'''
from .baseclient import BaseClient


'''有道客户端'''
class YoudaoClient(BaseClient):
    def __init__(self, reload_history=True, **kwargs):
        super(YoudaoClient, self).__init__(website_name='youdao', reload_history=reload_history, **kwargs)
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        url = 'http://dict.youdao.com/login/acc/query/accountinfo'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Host': 'dict.youdao.com',
            'Referer': 'http://dict.youdao.com/wordbook/wordlist?keyfrom=dict2.index'
        }
        response = session.get(url, headers=headers)
        response_json = response.json()
        if response_json['msg'] == 'OK' and response_json['code'] == 0:
            return False
        return True