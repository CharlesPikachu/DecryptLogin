'''
Function:
    requests模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-17
'''
import warnings
from .modules import *
warnings.filterwarnings('ignore')


'''模拟登录类-直接返回登录后的session'''
class Login():
    def __init__(self, disable_print_auth=False, **kwargs):
        if not disable_print_auth: print(self)
        self.supported_apis = {
            'douban': douban().login, 'weibo': weibo().login, 'github': github().login, 'music163': music163().login, 
            'zt12306': zt12306().login, 'QQZone': QQZone().login, 'QQQun': QQQun().login, 'QQId': QQId().login, 
            'zhihu': zhihu().login, 'bilibili': bilibili().login, 'toutiao': toutiao().login, 'taobao': taobao().login, 
            'jingdong': jingdong().login, 'ifeng': ifeng().login, 'sohu': sohu().login, 'zgconline': zgconline().login, 
            'lagou': lagou().login, 'twitter': twitter().login, 'eSurfing': eSurfing().login, 'tencentvideo': tencentvideo().login,
            'renren': renren().login, 'w3cschool': w3cschool().login, 'fishc': fishc().login, 'youdao': youdao().login, 
            'baidupan': baidupan().login, 'stackoverflow': stackoverflow().login, 'codalab': codalab().login, 'pypi': pypi().login, 
            'douyu': douyu().login, 'migu': migu().login, 'qunar': qunar().login, 'mieshop': mieshop().login, 'mpweixin': mpweixin().login, 
            'baidutieba': baidutieba().login, 'dazhongdianping': dazhongdianping().login, 'jianguoyun': jianguoyun().login, 
            'cloud189': cloud189().login, 'qqmusic': qqmusic().login, 'ximalaya': ximalaya().login, 'icourse163': icourse163().login, 
            'xiaomihealth': xiaomihealth().login,
        }
        for key, value in self.supported_apis.items():
            setattr(self, key, value)
    '''str'''
    def __str__(self):
        return 'Welcome to use DecryptLogin!\nYou can visit https://github.com/CharlesPikachu/DecryptLogin for more details.'


'''返回对应网站的客户端'''
class Client():
    def __init__(self, disable_print_auth=False, **kwargs):
        if not disable_print_auth: print(self)
        self.supported_clients = {
            'bilibili': BiliBiliClient, 'weibo': WeiboClient, 'douban': DoubanClient, 'github': GithubClient,
            'music163': Music163Client, 'zt12306': Zt12306Client, 'QQZone': QQZoneClient, 'QQId': QQIdClient,
            'QQQun': QQQunClient, 'zhihu': ZhihuClient, 'taobao': TaobaoClient, 'toutiao': ToutiaoClient,
            'jingdong': JingdongClient, 'ifeng': IfengClient, 'sohu': SohuClient, 'zgconline': ZgconlineClient,
            'twitter': TwitterClient, 'renren': RenRenClient, 'lagou': LagouClient, 'eSurfing': eSurfingClient,
            'w3cschool': W3CSchoolClient, 'fishc': FishCClient, 'youdao': YoudaoClient, 'stackoverflow': StackoverflowClient,
            'baidupan': BaiduPanClient, 'douyu': DouyuClient, 'codalab': CodaLabClient, 'pypi': PyPiClient,
            'migu': MiguClient, 'qunar': QunarClient, 'xiaomihealth': XiaomiHealthClient, 'mieshop': MieShopClient,
            'mpweixin': MpweixinClient, 'baidutieba': BaiduTiebaClient, 'dazhongdianping': DazhongdianpingClient, 'jianguoyun': JianguoyunClient,
            'cloud189': Cloud189Client, 'qqmusic': QQMusicClient, 'ximalaya': XimalayaClient, 'icourse163': Icourse163Client,
            'tencentvideo': TencentVideoClient,
        }
        for key, value in self.supported_clients.items():
            setattr(self, key, value)
    '''str'''
    def __str__(self):
        return 'Welcome to use DecryptLogin!\nYou can visit https://github.com/CharlesPikachu/DecryptLogin for more details.'