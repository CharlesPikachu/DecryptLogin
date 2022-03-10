'''
Function:
    requests模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-03-10
'''
from .modules import *


'''模拟登录类-直接返回登录后的session'''
class Login():
    def __init__(self, disable_print_auth=False, **kwargs):
        if not disable_print_auth: print(self)
        self.supported_apis = {
            'douban': douban().login, 'weibo': weibo().login, 'github': github().login, 'music163': music163().login, 
            'zt12306': zt12306().login, 'QQZone': QQZone().login, 'QQQun': QQQun().login, 'QQId': QQId().login, 
            'zhihu': zhihu().login, 'bilibili': bilibili().login, 'toutiao': toutiao().login, 'taobao': taobao().login, 
            'jingdong': jingdong().login, 'ifeng': ifeng().login, 'sohu': sohu().login, 'zgconline': zgconline().login, 
            'lagou': lagou().login, 'twitter': twitter().login, 'eSurfing': eSurfing().login, 
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


'''模拟登录器类-仅返回对应平台的实例化类'''
class Loginer():
    def __init__(self, **kwargs):
        if not disable_print_auth: print(self)
        self.supported_apis = {
            'douban': douban, 'weibo': weibo, 'github': github, 'music163': music163, 
            'zt12306': zt12306, 'QQZone': QQZone, 'QQQun': QQQun, 'QQId': QQId, 
            'zhihu': zhihu, 'bilibili': bilibili, 'toutiao': toutiao, 'taobao': taobao, 
            'jingdong': jingdong, 'ifeng': ifeng, 'sohu': sohu, 'zgconline': zgconline, 
            'lagou': lagou, 'twitter': twitter, 'eSurfing': eSurfing, 
            'renren': renren, 'w3cschool': w3cschool, 'fishc': fishc, 'youdao': youdao,
            'baidupan': baidupan, 'stackoverflow': stackoverflow, 'codalab': codalab, 'pypi': pypi, 
            'douyu': douyu, 'migu': migu, 'qunar': qunar, 'mieshop': mieshop, 'mpweixin': mpweixin, 
            'baidutieba': baidutieba, 'dazhongdianping': dazhongdianping, 'jianguoyun': jianguoyun, 
            'cloud189': cloud189, 'qqmusic': qqmusic, 'ximalaya': ximalaya, 'icourse163': icourse163, 
            'xiaomihealth': xiaomihealth,
        }
        for key, value in self.supported_apis.items():
            setattr(self, key, value)
    '''str'''
    def __str__(self):
        return 'Welcome to use DecryptLogin!\nYou can visit https://github.com/CharlesPikachu/DecryptLogin for more details.'