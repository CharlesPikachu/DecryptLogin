'''
Function:
    QQ个人专属报告
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import os
import time
import json
import random
import requests
from .utils import *
from DecryptLogin import login


'''QQ个人专属报告类'''
class QQReports():
    def __init__(self, savedir='qqdata', username='charlespikachu'):
        client = login.Client()
        # QQ空间
        infos_return, self.session_zone = client.QQZone(reload_history=True).login(username, '微信公众号: Charles的皮卡丘', 'scanqr')
        self.username = infos_return.get('username')
        self.session_zone_all_cookies = requests.utils.dict_from_cookiejar(self.session_zone.cookies)
        # QQ安全中心
        _, self.session_id = client.QQId(reload_history=True).login(username, '微信公众号: Charles的皮卡丘', 'scanqr')
        self.session_id_all_cookies = requests.utils.dict_from_cookiejar(self.session_id.cookies)
        # QQ群
        _, self.session_qun = client.QQQun(reload_history=True).login(username, '微信公众号: Charles的皮卡丘', 'scanqr')
        self.session_qun_all_cookies = requests.utils.dict_from_cookiejar(self.session_qun.cookies)
        # 数据保存的文件夹(方便后续的可视化操作)
        self.savedir = savedir
        touchdir(self.savedir)
    '''外部调用运行'''
    def run(self):
        # 一些常量
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        fontpath = os.path.join(rootdir, 'resources/font.TTF')
        # 个人基本信息
        personal_info = self.getPersonalInfo('personal_info.pkl')
        makePersonalCard(personal_info, os.path.join(rootdir, 'resources/personalcard.jpg'), savepath=os.path.join(self.savedir, 'personal_info.jpg'), fontpath=fontpath)
        # 好友信息
        friends_info = self.getQQFriendsInfo('friends_info.pkl')
        nicknames = [value[0] for value in friends_info.values()]
        nicknames = dict(zip(nicknames, [1]*len(nicknames)))
        drawWordCloud(nicknames, savepath=os.path.join(self.savedir, 'friends_info.jpg'), font_path=fontpath)
        # 最近操作信息
        recent_operation_info = self.getRecentOperationsInfo('recent_operation_info.pkl')
        makeRecentCard(friends_info, recent_operation_info, os.path.join(rootdir, 'resources/recentcard.jpg'), savepath=os.path.join(self.savedir, 'recent_operation_info.jpg'), fontpath=fontpath)
    '''获取登录账户的个人资料'''
    def getPersonalInfo(self, filename='personal_info.pkl'):
        personal_info = dict()
        summary_url = 'https://id.qq.com/cgi-bin/summary?'
        userinfo_url = 'https://id.qq.com/cgi-bin/userinfo?'
        bkn = self.__skey2bkn(self.session_id_all_cookies['skey'])
        params = {
            'r': str(random.random()),
            'ldw': str(bkn)
        }
        headers = {
            'referer': 'https://id.qq.com/myself/myself.html?ver=10049&',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        response = self.session_id.get(summary_url, headers=headers, params=params, verify=False)
        response.encoding = 'utf-8'
        personal_info.update(response.json())
        params = {
            'r': str(random.random()),
            'ldw': str(bkn)
        }
        headers = {
            'referer': 'https://id.qq.com/myself/myself.html?ver=10045&',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        while True:
            response = self.session_id.get(userinfo_url, headers=headers, params=params, verify=False)
            response.encoding = 'utf-8'
            if response.text:
                break
        personal_info.update(response.json())
        personal_info_parsed = {
            '昵称': personal_info['nick'],
            '出生日期': '-'.join([str(personal_info['bir_y']), str(personal_info['bir_m']).zfill(2), str(personal_info['bir_d']).zfill(2)]),
            '年龄': personal_info['age'],
            'Q龄': personal_info['qq_age'],
            '账号等级': personal_info['level'],
            '等级排名': personal_info['level_rank'],
            '好友数量': personal_info['friend_count'],
            '单向好友数量': personal_info['odd_count'],
            '已备注好友数量': personal_info['remark_count'],
            '好友分组数量': personal_info['group_count'],
            '最近联系人数量': personal_info['chat_count'],
            '工作': personal_info['work'],
            '个性签名': personal_info['ln']
        }
        saveData2Pkl(personal_info_parsed, os.path.join(self.savedir, filename))
        return personal_info_parsed
    '''抓取QQ好友数据'''
    def getQQFriendsInfo(self, filename='friends_info.pkl'):
        friends_info = dict()
        bkn = self.__skey2bkn(self.session_zone_all_cookies['skey'])
        get_friend_list_url = f'https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?uin={self.username}&follow_flag=1&groupface_flag=0&fupdate=1&g_tk={bkn}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        response = self.session_zone.get(get_friend_list_url, verify=False, headers=headers)
        text = response.text.replace('_Callback(', '')
        for item in json.loads(text[:len(text)-2])['data']['items']:
            qq_number = item['uin']
            nickname = item['remark'] or item['name']
            friends_info[qq_number] = [nickname]
        saveData2Pkl(friends_info, os.path.join(self.savedir, filename))
        return friends_info
    '''获取近期的操作数据'''
    def getRecentOperationsInfo(self, filename='recent_operation_info.pkl'):
        recent_operation_info = dict()
        bkn = self.__skey2bkn(self.session_qun_all_cookies['skey'])
        # 近30天退出的群
        data = {'bkn': bkn}
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'origin': 'https://huifu.qq.com',
            'referer' : 'https://huifu.qq.com/recovery/index.html?frag=0',
            'content-type': 'text/plain'
        }
        gr_grouplist_url = 'https://huifu.qq.com/cgi-bin/gr_grouplist'
        response = self.session_qun.post(gr_grouplist_url, data=data, headers=headers, verify=False)
        group_info = response.json()
        recent_operation_info['过去30天我退出的群个数'] = len(group_info.get('ls', []))
        recent_operation_info['过去30天我退出的群'] = []
        if 'ls' in group_info.keys():
            for each in group_info['ls']:
                recent_operation_info['过去30天我退出的群'].append(str(each['n']))
        # 近一年删除的好友
        params = {
            'bkn': str(bkn),
            'ts': str(int(time.time())),
            'g_tk': str(bkn),
            'data': '{"11053":{"iAppId":1,"iKeyType":1,"sClientIp":"","sSessionKey":"%s","sUin":"%s"}}' % (self.session_qun_all_cookies['skey'], self.username)
        }
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'origin': 'https://huifu.qq.com',
            'referer' : 'https://huifu.qq.com/recovery/index.html?frag=1',
            'content-type': 'text/plain'
        }
        srfentry_url = 'https://proxy.vip.qq.com/cgi-bin/srfentry.fcgi?'
        response = self.session_qun.get(srfentry_url, params=params, headers=headers, verify=False)
        del_friend_list = response.json()['11053']['data']['delFriendList']
        recent_operation_info['过去一年我删除的好友个数'] = len(del_friend_list)
        recent_operation_info['过去一年我删除的好友'] = []
        if len(del_friend_list) > 0:
            recent_operation_info['过去一年我删除的好友'] = [str(each) for each in del_friend_list['364']['vecUin']]
        # 谁在意我
        bkn = self.__skey2bkn(self.session_zone_all_cookies['skey'])
        url = f'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={self.username}&do=2&rd=0.6629930546880991&fupdate=1&clean=1&g_tk={bkn}&g_tk={bkn}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        response = self.session_zone.get(url, verify=False, headers=headers)
        text = response.text.replace('_Callback(', '')
        who_care_me = json.loads(text[:len(text)-2])['data']['items_list']
        if len(who_care_me) > 5:
            who_care_me = who_care_me[:5]
        recent_operation_info['谁在意我'] = [[each['uin'], each['score']] for each in who_care_me]
        # 我在意谁
        url = f'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={self.username}&do=1&rd=0.6629930546880991&fupdate=1&clean=1&g_tk={bkn}&g_tk={bkn}'
        response = self.session_zone.get(url, verify=False, headers=headers)
        text = response.text.replace('_Callback(', '')
        i_care_who = json.loads(text[:len(text)-2])['data']['items_list']
        if len(i_care_who) > 5:
            i_care_who = i_care_who[:5]
        recent_operation_info['我在意谁'] = [[each['uin'], each['score']] for each in i_care_who]
        saveData2Pkl(recent_operation_info, os.path.join(self.savedir, filename))
        return recent_operation_info
    '''根据skey参数得到bkn参数'''
    def __skey2bkn(self, skey):
        bkn = 5381
        for c in skey:
            bkn += (bkn << 5) + ord(c)
        return 2147483647 & bkn