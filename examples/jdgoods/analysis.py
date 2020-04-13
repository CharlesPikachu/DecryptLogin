'''
Function:
    京东商品数据可视化, pyecharts版本: 1.5.1
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pickle
from pyecharts import options
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Pie, Funnel


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
          .set_global_opts(xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-15)),
                           title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    bar.render(os.path.join(savedir, title+'.html'))


'''画漏斗图'''
def drawFunnel(title, data, savedir='./results'):
    checkDir(savedir)
    funnel = (Funnel(init_opts=options.InitOpts(theme=ThemeType.MACARONS))
             .add('', [list(item) for item in data.items()], label_opts=options.LabelOpts(position="inside"))
             .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    funnel.render(os.path.join(savedir, title+'.html'))


'''run'''
if __name__ == '__main__':
    goods_infos_dict = pickle.load(open('无人机.pkl', 'rb'))
    # 自营店与非自营店比例
    data = {'自营店': 0, '非自营店': 0}
    for key, value in goods_infos_dict.items():
        if value['self_run']:
            data['自营店'] += 1
        else:
            data['非自营店'] += 1
    drawPie('自营店与非自营店比例', data)
    # 商品排名前10的店的商品评论数量/评论排名前10的店铺
    data = {}
    for key, value in goods_infos_dict.items():
        if not value['shop_name'] or not value['good_rate']:
            continue
        data[value['shop_name']] = [int(value['num_comments']), int(value['good_rate'])]
    data_gr = dict(sorted(data.items(), key=lambda item: item[1][1])[:10])
    data_ct = dict(sorted(data.items(), key=lambda item: -item[1][0])[:10])
    data_gr_filter = {}
    for key, value in data_gr.items():
        data_gr_filter[key] = value[0]
    data_ct_filter = {}
    for key, value in data_ct.items():
        data_ct_filter[key] = value[0]
    drawBar('商品排名前10的店的商品评论数量', data_gr_filter)
    drawBar('评论排名前10的店铺', data_ct_filter)
    # 无人机相关商品的价格分布
    data = {'100元以内': 0, '100-300元': 0, '300-500元': 0, '500-1000元': 0, '1000-2000元': 0, '2000元以上': 0}
    for key, value in goods_infos_dict.items():
        price = float(value['price'])
        if price < 100:
            data['100元以内'] += 1
        elif price >= 100 and price < 300:
            data['100-300元'] += 1
        elif price >= 300 and price < 500:
            data['300-500元'] += 1
        elif price >= 500 and price < 1000:
            data['500-1000元'] += 1
        elif price >= 1000 and price < 2000:
            data['1000-2000元'] += 1
        elif price >= 2000:
            data['2000元以上'] += 1
    drawFunnel('无人机相关商品的价格分布', data)