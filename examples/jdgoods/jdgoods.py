'''
Function:
    京东商品数据小爬虫
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import pickle
import random
from DecryptLogin import login


'''京东商品数据小爬虫'''
class JDGoodsCrawler():
    def __init__(self, **kwargs):
        if os.path.isfile('session.pkl'):
            print('[INFO]: 检测到已有会话文件session.pkl, 将直接导入该文件...')
            self.session = pickle.load(open('session.pkl', 'rb'))
            self.session.headers.update({'Referer': ''})
        else:
            self.session = JDGoodsCrawler.login()
            f = open('session.pkl', 'wb')
            pickle.dump(self.session, f)
            f.close()
    '''外部调用'''
    def run(self):
        search_url = 'https://search-x.jd.com/Search?'
        while True:
            goods_name = input('请输入想要抓取的商品信息名称: ')
            goods_infos_dict = {}
            page_interval = random.randint(1, 5)
            page_count = 1
            page_pointer = 1
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
                    goods_infos_dict.update({len(goods_infos_dict)+1: 
                                                {
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
                print(goods_infos_dict)
                self.__save(goods_infos_dict, goods_name+'.pkl')
                page_count += 1
                page_pointer += 1
                if page_pointer == page_interval:
                    time.sleep(random.randint(50, 60)+random.random()*10)
                    page_interval = random.randint(2, 5)
                    page_pointer = 0
                else:
                    time.sleep(random.random()+1)
            print('[INFO]: 关于%s的商品数据抓取完毕, 共抓取到%s条数据...' % (goods_name, len(goods_infos_dict)))
    '''数据保存'''
    def __save(self, data, savepath):
        fp = open(savepath, 'wb')
        pickle.dump(data, fp)
        fp.close()
    '''模拟登录京东'''
    @staticmethod
    def login():
        lg = login.Login()
        infos_return, session = lg.jingdong()
        return session


'''run'''
if __name__ == '__main__':
    crawler = JDGoodsCrawler()
    crawler.run()