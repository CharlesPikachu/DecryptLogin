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
          .set_global_opts(xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-30)),
                           title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    bar.render(os.path.join(savedir, title+'.html'))


'''画漏斗图'''
def drawFunnel(title, data, savedir='./results'):
    checkDir(savedir)
    funnel = (Funnel(init_opts=options.InitOpts(theme=ThemeType.MACARONS))
             .add('', [list(item) for item in data.items()], label_opts=options.LabelOpts(position="inside"))
             .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    funnel.render(os.path.join(savedir, title+'.html'))


'''画地图'''
def drawMap(title, data, savedir='./results'):
    checkDir(savedir)
    map_ = (Map(init_opts=options.InitOpts(theme=ThemeType.ROMANTIC)))
           .add('', [list(item) for item in data.items()], 'china')
           .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    map_.render(os.path.join(savedir, title+'.html'))


'''run'''
if __name__ == '__main__':
    goods_infos_dict = pickle.load(open('奶茶.pkl', 'rb'))
    # 奶茶店分布
    # 