'''
Function:
    requests模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
from .core import *


'''模拟登录类-直接返回登录后的session'''
class Login():
    def __init__(self, **kwargs):
        self.info = 'Login class, login in some websites using requests directly.'
        self.supported_apis = {
            'douban': douban().login, 'weibo': weibo().login, 'github': github().login, 'music163': music163().login, 
            'zt12306': zt12306().login, 'QQZone': QQZone().login, 'QQQun': QQQun().login, 'QQId': QQId().login, 
            'zhihu': zhihu().login, 'bilibili': bilibili().login, 'toutiao': toutiao().login, 'taobao': taobao().login, 
            'jingdong': jingdong().login, 'ifeng': ifeng().login, 'sohu': sohu().login, 'zgconline': zgconline().login, 
            'lagou': lagou().login, 'twitter': twitter().login, 'vultr': vultr().login, 'eSurfing': eSurfing().login, 
            'renren': renren().login, 'w3cschool': w3cschool().login, 'fishc': fishc().login, 'youdao': youdao().login, 
            'baidupan': baidupan().login, 'stackoverflow': stackoverflow().login, 'codalab': codalab().login, 'pypi': pypi().login, 
            'xiami': xiami().login, 'douyu': douyu().login, 'migu': migu().login, 'qunar': qunar().login, 
            'mieshop': mieshop().login, 'mpweixin': mpweixin().login, 'baidutieba': baidutieba().login, 'dazhongdianping': dazhongdianping().login,
            'jianguoyun': jianguoyun().login, 'cloud189': cloud189().login, 'qqmusic': qqmusic().login
        }
        for key, value in self.supported_apis.items():
            setattr(self, key, value)


'''模拟登录器类-仅返回对应平台的实例化类'''
class Loginer():
    def __init__(self, **kwargs):
        self.info = 'Loginer class, returning the instantiated website loginers.'
        self.supported_apis = {
            'douban': douban, 'weibo': weibo, 'github': github, 'music163': music163, 
            'zt12306': zt12306, 'QQZone': QQZone, 'QQQun': QQQun, 'QQId': QQId, 
            'zhihu': zhihu, 'bilibili': bilibili, 'toutiao': toutiao, 'taobao': taobao, 
            'jingdong': jingdong, 'ifeng': ifeng, 'sohu': sohu, 'zgconline': zgconline, 
            'lagou': lagou, 'twitter': twitter, 'vultr': vultr, 'eSurfing': eSurfing, 
            'renren': renren, 'w3cschool': w3cschool, 'fishc': fishc, 'youdao': youdao,
            'baidupan': baidupan, 'stackoverflow': stackoverflow, 'codalab': codalab, 'pypi': pypi, 
            'xiami': xiami, 'douyu': douyu, 'migu': migu, 'qunar': qunar, 
            'mieshop': mieshop, 'mpweixin': mpweixin, 'baidutieba': baidutieba, 'dazhongdianping': dazhongdianping,
            'jianguoyun': jianguoyun, 'cloud189': cloud189, 'qqmusic': qqmusic
        }
        for key, value in self.supported_apis.items():
            setattr(self, key, value)