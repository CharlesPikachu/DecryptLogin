'''
Function:
    淘宝商品数据小爬虫
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import json
import pickle
import random
from DecryptLogin import login


'''淘宝商品数据小爬虫'''
class TBGoods():
    def __init__(self, username='charlespikachu'):
        self.username = username
        self.session = self.login()
    '''外部调用'''
    def run(self):
        search_url = 'https://s.taobao.com/search?'
        while True:
            goods_name = input('请输入想要抓取的商品信息名称: ')
            goods_infos_dict = {}
            page_interval, page_pointer, offset, page_size = random.randint(1, 5), 0, 0, 44
            while True:
                params = {
                    'q': goods_name,
                    'commend': 'all',
                    'ssid': 's5-e',
                    'search_type': 'item',
                    'sourceId': 'tb.index',
                    'spm': 'a21bo.jianhua.201856-taobao-item.2',
                    'ie': 'utf8',
                    'initiative_id': 'tbindexz_20170306',
                }
                response = self.session.get(search_url, params=params)
                if (response.status_code != 200): break
                response_json = json.loads(re.findall(r'g_page_config = (\{.*?\});', response.text)[0])
                all_items = response_json.get('mods', {}).get('itemlist', {}).get('data', {}).get('auctions', [])
                if len(all_items) == 0:
                    break
                for item in all_items:
                    if not item['category']:
                        continue
                    goods_infos_dict.update({
                        len(goods_infos_dict)+1: {
                            'shope_name': item.get('nick', ''),
                            'title': item.get('raw_title', ''),
                            'pic_url': item.get('pic_url', ''),
                            'detail_url': item.get('detail_url', ''),
                            'price': item.get('view_price', ''),
                            'location': item.get('item_loc', ''),
                            'fee': item.get('view_fee', ''),
                            'num_comments': item.get('comment_count', ''),
                            'num_sells': item.get('view_sales', '')
                        }
                    })
                self.logging(goods_infos_dict)
                self.save(goods_infos_dict, goods_name+'.pkl')
                offset += page_size
                if offset // page_size > 100:
                    break
                page_pointer += 1
                if page_pointer == page_interval:
                    time.sleep(random.randint(30, 60)+random.random()*10)
                    page_interval = random.randint(1, 5)
                    page_pointer = 0
                else:
                    time.sleep(random.random()+2)
            self.logging('关于%s的商品数据抓取完毕, 共抓取到%s条数据' % (goods_name, len(goods_infos_dict)))
    '''数据保存'''
    def save(self, data, savepath):
        fp = open(savepath, 'wb')
        pickle.dump(data, fp)
        fp.close()
    '''模拟登录'''
    def login(self):
        client = login.Client()
        taobao = client.taobao(reload_history=True)
        infos_return, session = taobao.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')