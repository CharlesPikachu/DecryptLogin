'''
Function:
    京东抢购脚本
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import random
import pyttsx3
import requests
from bs4 import BeautifulSoup
from DecryptLogin import login
from prettytable import PrettyTable


'''京东抢购脚本'''
class JingDongSnap():
    def __init__(self, username='charlespikachu', trybuy_interval=1800, server_key=None, paywd=None):
        self.username = username
        self.session = self.login()
        self.trybuy_interval = int(trybuy_interval)
        self.server_key = server_key
        self.paywd = paywd
    '''运行'''
    def run(self):
        # 获得购物车信息
        cart_infos = self.buycartinfo()
        # 打印并选择想要抢购的商品信息
        title, items = ['id', 'title'], []
        for key, value in cart_infos.items():
            items.append([key, value['title']])
        self.printTable(title, items)
        good_id = input('请选择想要抢购的商品编号(例如"0"): ')
        assert good_id in cart_infos, '输入的商品编号有误'
        # 根据选择尝试购买商品
        self.logging(f'正在尝试抢购商品***{cart_infos[good_id]["title"]}***')
        while True:
            try:
                is_success = self.buygood(cart_infos[good_id])
            except:
                is_success = False
            if is_success: break
            time.sleep(self.trybuy_interval)
            self.logging(f'抢购***{cart_infos[good_id]["title"]}***失败, 将在{self.trybuy_interval}秒后重新尝试下单.')
        self.logging(f'抢购***{cart_infos[good_id]["title"]}***成功, 已为您自动提交订单, 请尽快前往京东完成付款.')
        # 电脑语音提示
        for _ in range(5):
            pyttsx3.speak('已经为您抢购到你所需的商品, 请尽快前往京东完成付款.')
        # 发送Server酱提示
        if self.server_key:
            self.pushwechat(f'已经为您抢购到你所需的商品***{cart_infos[good_id]["title"]}***, 请尽快前往京东完成付款.')
    '''获得购物车信息'''
    def buycartinfo(self):
        cart_url = 'https://api.m.jd.com/api?'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'origin': 'https://cart.jd.com',
            'Referer': 'https://cart.jd.com',
        }
        data = {
            'functionId': 'pcCart_jc_getCurrentCart',
            'appid': 'JDC_mall_cart',
            'loginType': '3',
        }
        response = self.session.post(cart_url, headers=headers, data=data)
        response_json, cart_infos = response.json(), {}
        for idx, item in enumerate(response_json['resultData']['cartInfo']['vendors']):
            cart_info = {
                'title': self.rematch(r"'Name': '(.*?)',", str(item)),
                'Id': item['sorted'][0]['item']['Id'],
                'skuUuid': self.rematch(r"'skuUuid': '(.*?)',", str(item)),
                'IdForOldVersion': self.rematch(r"'IdForOldVersion': (.*?),", str(item)),
                'SType': '11',
            }
            cart_infos[str(idx)] = cart_info
        return cart_infos
    '''利用正则表达式获得有效信息'''
    def rematch(self, pattern, string):
        all_finds = re.findall(pattern, string)
        for item in all_finds:
            if item: return item
        return ''
    '''购买商品'''
    def buygood(self, good_info):
        # 取消勾选购物车中的所有商品
        url = 'https://cart.jd.com/cancelAllItem.action'
        data = {
            't': 0,
            'outSkus': '',
            'random': random.random(),
        }
        response = self.session.post(url, data=data)
        # 勾选指定商品商品
        url = 'https://api.m.jd.com/api'
        body = '{"operations":[{"ThePacks":[{"num":1,"sType":%s,"Id":%s,"TheSkus":[{"num":1,"Id":"%s","skuUuid":"%s","useUuid":false}]}]}]}' % \
            (good_info['SType'], good_info['Id'], good_info['IdForOldVersion'], good_info['skuUuid'])
        data = {
            'functionId': 'pcCart_jc_cartCheckSingle',
            'appid': 'JDC_mall_cart',
            'body': body,
            'loginType': '3',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'origin': 'https://cart.jd.com',
            'Referer': 'https://cart.jd.com',
        }
        response = self.session.post(url, data=data, headers=headers)
        # 获取订单结算页面信息
        url = 'http://trade.jd.com/shopping/order/getOrderInfo.action'
        params = {
            'rid': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://cart.jd.com/cart.action',
            'Connection': 'keep-alive',
            'Host': 'trade.jd.com'
        }
        response = self.session.get(url=url, params=params, headers=headers)
        if '刷新太频繁了' in response.text:
            raise RuntimeError('刷新太频繁了')
        if response.status_code != requests.codes.OK:
            raise RuntimeError('当前请求存在错误')
        soup = BeautifulSoup(response.text, 'html.parser')
        risk_control = soup.select('input#riskControl')[0].get('value').strip(' \t\r\n')
        order_detail = {
            'address': soup.find('span', id='sendAddr').text[5:],
            'receiver': soup.find('span', id='sendMobile').text[4:],
            'total_price': soup.find('span', id='sumPayPriceId').text[1:],
            'items': []
        }
        # 提交订单
        url = 'https://trade.jd.com/shopping/order/submitOrder.action'
        data = {
            'overseaPurchaseCookies': '',
            'vendorRemarks': '[]',
            'submitOrderParam.sopNotPutInvoice': 'false',
            'submitOrderParam.trackID': 'TestTrackId',
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'riskControl': order_detail,
            'submitOrderParam.isBestCoupon': '1',
            'submitOrderParam.jxj': '1',
            'submitOrderParam.trackId': '9643cbd55bbbe103eef18a213e069eb0',
            'submitOrderParam.needCheck': '1',
        }
        if self.paywd is not None:
            data['submitOrderParam.payPassword'] = ''.join(['u3' + x for x in self.paywd])
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Host': 'trade.jd.com',
            'Referer': 'http://trade.jd.com/shopping/order/getOrderInfo.action',
        }
        response = self.session.post(url=url, data=data, headers=headers)
        response_json = response.json()
        if response_json.get('success'): return True
        return False
    '''发送Server酱提示'''
    def pushwechat(self, desp='已经为您抢购到你所需的商品, 请尽快前往京东完成付款.'):
        server_url = f'https://sc.ftqq.com/{self.server_key}.send'
        params = {
            'text': '商品抢购成功提示',
            'desp': desp,
        }
        response = requests.get(server_url, params=params)
        return response
    '''打印表格'''
    def printTable(self, title, items):
        assert isinstance(title, list) and isinstance(items, list), 'title and items should be list...'
        table = PrettyTable(title)
        for item in items: table.add_row(item)
        print(table)
        return table
    '''模拟登录'''
    def login(self):
        client = login.Client()
        jingdong = client.jingdong(reload_history=True)
        infos_return, session = jingdong.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')