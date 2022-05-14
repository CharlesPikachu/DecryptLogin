'''
Function:
    京东商品数据小爬虫
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import time
import pickle
import random
from DecryptLogin import login


'''京东商品数据小爬虫'''
class JDGoods():
    def __init__(self, username='charlespikachu'):
        self.username = username
        self.session = self.login()
    '''外部调用'''
    def run(self):
        search_url = 'https://search-x.jd.com/Search?'
        while True:
            goods_name = input('请输入想要抓取的商品信息名称: ')
            goods_infos_dict = {}
            page_count, page_pointer, page_interval = 1, 1, random.randint(1, 5)
            while True:
                params = {
                    'area': '15',
                    'enc': 'utf-8',
                    'keyword': goods_name,
                    'adType': '7',
                    'page': str(page_count),
                    'ad_ids': '291:19',
                    'xtest': 'new_search',
                    '_': str(int(time.time()*1000))
                }
                response = self.session.get(search_url, params=params)
                if (response.status_code != 200):
                    break
                response_json = response.json()
                all_items = response_json.get('291', [])
                if len(all_items) == 0:
                    break
                for item in all_items:
                    goods_infos_dict.update({
                        len(goods_infos_dict)+1: {
                            'image_url': item.get('image_url', ''),
                            'price': item.get('pc_price', ''),
                            'shop_name': item.get('shop_link', {}).get('shop_name', ''),
                            'num_comments': item.get('comment_num', ''),
                            'link_url': item.get('link_url', ''),
                            'color': item.get('color', ''),
                            'title': item.get('ad_title', ''),
                            'self_run': item.get('self_run', ''),
                            'good_rate': item.get('good_rate', '')
                        }
                    })
                self.logging(goods_infos_dict)
                self.save(goods_infos_dict, goods_name+'.pkl')
                page_count += 1
                page_pointer += 1
                if page_pointer == page_interval:
                    time.sleep(random.randint(50, 60)+random.random()*10)
                    page_interval = random.randint(2, 5)
                    page_pointer = 0
                else:
                    time.sleep(random.random()+1)
            self.logging('关于%s的商品数据抓取完毕, 共抓取到%s条数据' % (goods_name, len(goods_infos_dict)))
    '''数据保存'''
    def save(self, data, savepath):
        fp = open(savepath, 'wb')
        pickle.dump(data, fp)
        fp.close()
    '''模拟登录'''
    def login(self):
        client = login.Client()
        jingdong = client.jingdong(reload_history=True)
        infos_return, session = jingdong.login(self.username, '微信公众号: Charles的皮卡丘', 'scanqr')
        return session
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')