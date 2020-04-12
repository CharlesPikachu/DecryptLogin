'''
Function:
    淘宝商品数据可视化, pyecharts版本: 1.5.1
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pickle
from pyecharts import options
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Page, Pie, Map


'''检查文件在是否存在'''
def checkDir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        return False
    return True


'''画饼图'''
def drawPie(title, data, savedir='./results'):
    checkDir(savedir)
    pie = (Pie(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
          .add('', [list(item) for item in data.items()], radius=['30%', '75%'], center=['50%', '50%'], rosetype='radius')
          .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='5%', pos_left='2%')))
    pie.render(os.path.join(savedir, title+'.html'))


'''画柱状图'''
def drawBar(title, data, savedir='./results'):
    checkDir(savedir)
    bar = (Bar(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
          .add_xaxis(list(data.keys()))
          .add_yaxis('', list(data.values()))
          .set_global_opts(xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-25)),
                           title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    bar.render(os.path.join(savedir, title+'.html'))


'''画地图'''
def drawMap(title, data, savedir='./results'):
    checkDir(savedir)
    map_ = (Map(init_opts=options.InitOpts(theme=ThemeType.ROMANTIC))
           .add('', [list(item) for item in data.items()], 'china')
           .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), visualmap_opts=options.VisualMapOpts(max_=max(list(data.values())), min_=min(list(data.values())), is_show=True)))
    map_.render(os.path.join(savedir, title+'.html'))


'''run'''
if __name__ == '__main__':
    goods_infos_dict = pickle.load(open('奶茶.pkl', 'rb'))
    # 淘宝上卖奶茶的商家在全国范围内的数量​分布情况
    data = {}
    for key, value in goods_infos_dict.items():
        location = value['location'].split(' ')[0]
        if location in data:
            data[location] += 1
        else:
            data[location] = 1
    drawMap(title='淘宝上卖奶茶的商家在全国范围内的数量​分布情况', data=data)
    # 淘宝上卖奶茶的​店铺的销量排名前10
    data = {}
    for key, value in goods_infos_dict.items():
        num_sells = value['num_sells']
        if not num_sells:
           continue
        if u'万' in num_sells:
            num_sells = float(num_sells.replace(u'万+人付款', '').strip()) * 1e4
        else:
            num_sells = float(num_sells.replace(u'人付款', '').replace(u'+', '').strip())
        if value['shope_name'] in data:
            data[value['shope_name']] += num_sells
        else:
            data[value['shope_name']] = num_sells
    data = dict(sorted(data.items(), key=lambda item: item[1])[-10:])
    drawBar('淘宝上卖奶茶的​店铺的销量排名前10', data)
    # 淘宝上评论数量前10名的奶茶店铺
    data = {}
    for key, value in goods_infos_dict.items():
        num_comments = value['num_comments']
        if not num_comments:
           continue
        num_comments = float(num_comments)
        if value['shope_name'] in data:
            data[value['shope_name']] += num_comments
        else:
            data[value['shope_name']] = num_comments
    data = dict(sorted(data.items(), key=lambda item: item[1])[-10:])
    drawBar('淘宝上评论数量前10名的奶茶店铺', data)
    # 要运费与免运费的奶茶相关商品比例
    data = {'fee': 0, 'no_fee': 0}
    for key, value in goods_infos_dict.items():
        if float(value['fee']) > 0:
            data['fee'] += 1
        else:
            data['no_fee'] += 1
    drawPie('要运费与免运费的奶茶相关商品比例', data)
    # 奶茶相关商品的售价区间
    data = {'小于10元': 0, '10~30元': 0, '30~50元': 0, '50~100元': 0, '100元以上': 0}
    for key, value in goods_infos_dict.items():
        if not value['price']:
            continue
        price = float(value['price'])
        if price < 10:
            data['小于10元'] += 1
        elif price >= 10 and price <= 30:
            data['10~30元'] += 1
        elif price > 30 and price <= 50:
            data['30~50元'] += 1
        elif price > 50 and price <= 100:
            data['50~100元'] += 1
        else:
            data['100元以上'] += 1
    drawPie('奶茶相关商品的售价区间', data)