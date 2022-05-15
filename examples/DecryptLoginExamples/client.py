'''
Function:
    模拟登录系列爬虫调用客户端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import warnings
try: from .crawlers import *
except: from crawlers import *
warnings.filterwarnings('ignore')


'''模拟登录系列爬虫调用客户端'''
class Client():
    def __init__(self, disable_print_auth=True, **kwargs):
        if not disable_print_auth: print(self)
        self.supported_crawlers = {
            'bilibililottery': BiliBiliLottery, 'weiboemoji': WeiboEmoji, 'weiboblacklist': WeiboBlackList, 'weibowater': WeiboWater,
            'weibosender': WeiboSender, 'weibomonitor': WeiboMonitor, 'userweibospider': UserWeiboSpider, 'delallweibos': DelAllWeibos,
            'cloud189signin': Cloud189Signin, 'clearqzone': ClearQzone, 'moocdl': MOOCDL, 'bilibiliupmonitor': BilibiliUPMonitor,
            'bilibiliuservideos': BilibiliUserVideos, 'modifymihealthsteps': ModifyMiHealthSteps, 'neteaseeveryday': NeteaseEveryday,
            'neteaseclickplaylist': NeteaseClickPlaylist, 'neteaselistenleaderboard': NeteaseListenLeaderboard, 'neteasesignin': NeteaseSignin,
            'neteasesonglistdownloader': NeteaseSongListDownloader, 'tbgoods': TBGoods, 'jdgoods': JDGoods, 'jingdongsnap': JingDongSnap,
            'taobaosnap': TaobaoSnap, 'qqreports': QQReports, 'weibolottery': WeiboLottery,
        }
        for key, value in self.supported_crawlers.items():
            setattr(self, key, value)
    '''执行对应的爬虫'''
    def executor(self, crawler_type=None, config={}):
        crawler = self.supported_crawlers[crawler_type](**config)
        return crawler.run()
    '''str'''
    def __str__(self):
        return 'Welcome to use DecryptLogin-examples!\nYou can visit https://github.com/CharlesPikachu/DecryptLogin for more details.'