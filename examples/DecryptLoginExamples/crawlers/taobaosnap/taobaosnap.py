'''
Function:
    淘宝抢购脚本
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import json
import urllib
import pyttsx3
import requests
from DecryptLogin import login
from prettytable import PrettyTable


'''淘宝抢购脚本'''
class TaobaoSnap():
    def __init__(self, username='charlespikachu', trybuy_interval=1800, server_key=None):
        self.username = username
        self.session = self.login()
        self.trybuy_interval = int(trybuy_interval)
        self.server_key = server_key
    '''运行'''
    def run(self):
        # 获得购物车信息
        cart_infos, user_id = self.buycartinfo()
        # 解析购物车信息
        if not cart_infos['success']:
            raise RuntimeError('获取购物车信息失败, 请尝试删除cookie缓存文件后重新扫码登录')
        if len(cart_infos['list']) == 0:
            raise RuntimeError('购物车是空的, 请在购物车中添加需要抢购的商品')
        good_infos = {}
        for idx, item in enumerate(cart_infos['list']):
            good_info = {
                'title': item['bundles'][0]['orders'][0]['title'],
                'cart_id': item['bundles'][0]['orders'][0]['cartId'],
                'cart_params': item['bundles'][0]['orders'][0]['cartActiveInfo']['cartBcParams'],
                'item_id': item['bundles'][0]['orders'][0]['itemId'],
                'sku_id': item['bundles'][0]['orders'][0]['skuId'],
                'seller_id': item['bundles'][0]['orders'][0]['sellerId'],
                'to_buy_info': item['bundles'][0]['orders'][0]['toBuyInfo'],
            }
            good_infos[str(idx)] = good_info
        # 打印并选择想要抢购的商品信息
        title, items = ['id', 'title'], []
        for key, value in good_infos.items():
            items.append([key, value['title']])
        self.printTable(title, items)
        good_id = input('请选择想要抢购的商品编号(例如"0"): ')
        assert good_id in good_infos, '输入的商品编号有误'
        # 根据选择尝试购买商品
        self.logging(f'正在尝试抢购商品***{good_infos[good_id]["title"]}***')
        while True:
            try:
                is_success = self.buygood(good_infos[good_id], user_id)
            except Exception as err:
                self.logging(f'抢购失败, 错误信息如下: \n{err}\n将在{self.trybuy_interval}秒后重新尝试.')
                is_success = False
            if is_success: break
            time.sleep(self.trybuy_interval)
        self.logging(f'抢购***{good_infos[good_id]["title"]}***成功, 已为您自动提交订单, 请尽快前往淘宝完成付款.')
        # 电脑语音提示
        for _ in range(5):
            pyttsx3.speak('已经为您抢购到你所需的商品, 请尽快前往淘宝完成付款.')
        # 发送Server酱提示
        if self.server_key:
            self.pushwechat(f'已经为您抢购到你所需的商品***{good_infos[good_id]["title"]}***, 请尽快前往淘宝完成付款.')
    '''发送Server酱提示'''
    def pushwechat(self, desp='已经为您抢购到你所需的商品, 请尽快前往淘宝完成付款.'):
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
    '''获得购物车信息'''
    def buycartinfo(self):
        url = 'https://cart.taobao.com/cart.htm'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0'
        }
        response = self.session.get(url, headers=headers)
        response_json = re.search('try{var firstData = (.*?);}catch', response.text).group(1)
        response_json = json.loads(response_json)
        user_id = re.search('\|\^taoMainUser:(.*?):\^', response.headers['s_tag']).group(1)
        return response_json, user_id
    '''购买商品'''
    def buygood(self, info, user_id):
        # 发送结算请求
        url = 'https://buy.taobao.com/auction/order/confirm_order.htm?spm=a1z0d.6639537.0.0.undefined'
        headers = {
            'cache-control': 'max-age=0', 'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'origin': 'https://cart.taobao.com', 'content-type': 'application/x-www-form-urlencoded',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document', 'referer': 'https://cart.taobao.com/',
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        cart_id, item_id, sku_id, seller_id, cart_params, to_buy_info = info['cart_id'], info['item_id'], info['sku_id'], info['seller_id'], info['cart_params'], info['to_buy_info']
        data = {
            'item': f'{cart_id}_{item_id}_1_{sku_id}_{seller_id}_0_0_0_{cart_params}_{urllib.parse.quote(str(to_buy_info))}__0',
            'buyer_from': 'cart',
            'source_time': ''.join(str(int(time.time() * 1000)))
        }
        response = self.session.post(url = url, data = data, headers = headers, verify = False)
        order_info = re.search('orderData= (.*?);\n</script>', response.text).group(1)
        order_info = json.loads(order_info)
        # 发送提交订单请求
        token = self.session.cookies['_tb_token_']
        endpoint = order_info['endpoint']
        data = order_info['data']
        structure = order_info['hierarchy']['structure']
        hierarchy = order_info['hierarchy']
        linkage = order_info['linkage']
        linkage.pop('url')
        submitref = order_info['data']['submitOrderPC_1']['hidden']['extensionMap']['secretValue']
        sparam1 = order_info['data']['submitOrderPC_1']['hidden']['extensionMap']['sparam1']
        input_charset = order_info['data']['submitOrderPC_1']['hidden']['extensionMap']['input_charset']
        event_submit_do_confirm = order_info['data']['submitOrderPC_1']['hidden']['extensionMap']['event_submit_do_confirm']
        url = f'https://buy.taobao.com/auction/confirm_order.htm?x-itemid={item_id}&x-uid={user_id}&submitref={submitref}&sparam1={sparam1}'
        data_submit = {}
        for key, value in data.items():
            if value.get('submit') == 'true' or value.get('submit'):
                data_submit[key] = value
        data = {
            'action': '/order/multiTerminalSubmitOrderAction', 
            '_tb_token_': token, 
            'event_submit_do_confirm': '1',
            'praper_alipay_cashier_domain': 'cashierrz54', 
            'input_charset': 'utf-8',
            'endpoint': urllib.parse.quote(json.dumps(endpoint)), 
            'data': urllib.parse.quote(json.dumps(data_submit)),
            'hierarchy': urllib.parse.quote(json.dumps({"structure": structure})), 
            'linkage': urllib.parse.quote(json.dumps(linkage))
        }
        headers = {
            'cache-control': 'max-age=0', 'upgrade-insecure-requests': '1', 'origin': 'https://buy.taobao.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://buy.taobao.com/auction/order/confirm_order.htm?spm=a1z0d.6639537.0.0.undefined',
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200: return True
        return False
    '''模拟登录'''
    def login(self):
        client = login.Client()
        taobao = client.taobao(reload_history=True)
        infos_return, session = taobao.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')