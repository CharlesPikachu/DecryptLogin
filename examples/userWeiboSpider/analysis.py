'''
Function:
	微博数据可视化, pyecharts版本: 1.5.1
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import jieba
import pickle
from pyecharts import options
from wordcloud import WordCloud
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie, Bar, Funnel


'''检查文件在是否存在'''
def checkDir(dirpath):
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
		return False
	return True


'''画饼图'''
def drawPie(title, data, savepath='./results'):
	checkDir(savepath)
	pie = (Pie(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
		  .add('', [list(item) for item in data.items()], radius=['30%', '75%'], center=['50%', '50%'], rosetype='radius')
		  .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='5%', pos_left='2%')))
	pie.render(os.path.join(savepath, title+'.html'))


'''画柱状图'''
def drawBar(title, data, savepath='./results'):
	checkDir(savepath)
	bar = (Bar(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
		  .add_xaxis(list(data.keys()))
		  .add_yaxis('', list(data.values()))
		  .set_global_opts(xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-30)),
		  				   title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
	bar.render(os.path.join(savepath, title+'.html'))


'''画漏斗图'''
def drawFunnel(title, data, savepath='./results'):
	checkDir(savepath)
	funnel = (Funnel(init_opts=options.InitOpts(theme=ThemeType.MACARONS))
			 .add('', [list(item) for item in data.items()], label_opts=options.LabelOpts(position="inside"))
			 .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
	funnel.render(os.path.join(savepath, title+'.html'))


'''统计词频'''
def statisticsWF(texts, stopwords):
	words_dict = {}
	for text in texts:
		if not text:
			continue
		for t in jieba.cut(text):
			if t in stopwords:
				continue
			if t in words_dict.keys():
				words_dict[t] += 1
			else:
				words_dict[t] = 1
	return words_dict


'''词云'''
def drawWordCloud(words, title, savepath='./results'):
	checkDir(savepath)
	wc = WordCloud(font_path='simkai.ttf', background_color='white', max_words=2000, width=1920, height=1080, margin=5)
	wc.generate_from_frequencies(words)
	wc.to_file(os.path.join(savepath, title+'.png'))


'''run'''
if __name__ == '__main__':
	# 数据读取
	f = open('datas/3261134763.pkl', 'rb')
	all_data = pickle.load(f)
	f.close()
	# 词云
	stopwords = open('./stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
	weibo_texts = []
	for key, value in all_data.items():
		if not value[0]:
			continue
		weibo_texts.append(value[-1].replace('宋承宪', '').replace('@', '').replace('cn', '').replace('#', '').replace('[', '').replace(']', '')\
									.replace('(', '').replace(')', '').replace('http', '').replace('/', '').replace('|', '').replace('<', '')\
									.replace('>', '').replace('（', '').replace('）', '').replace('原图', '').replace('原文', '').replace('转发', '')\
									.replace('评论', ''))
	drawWordCloud(statisticsWF(weibo_texts, stopwords=stopwords), title='原创微博内容词云')
	# 原创与非原创
	data = {'原创微博数量': 0, '非原创微博数量': 0}
	for key, value in all_data.items():
		if value[0]:
			data['原创微博数量'] += 1
		else:
			data['非原创微博数量'] += 1
	drawPie(title='原创与非原创微博数量对比', data=data)
	# 每年发的微博数量
	data = {}
	for key, value in all_data.items():
		year = value[1].split('-')[0]
		if year in data:
			data[year] += 1
		else:
			data[year] = 1
	data = dict(sorted(data.items(), key=lambda i: i[0]))
	drawBar(title='每年发的微博数量统计', data=data)
	# 点赞量统计
	data = {}
	for key, value in all_data.items():
		if not value[0]:
			continue
		year = value[1].split('-')[0]
		if year in data:
			data[year] += value[2]
		else:
			data[year] = value[2]
	data = dict(sorted(data.items(), key=lambda i: i[0]))
	drawBar(title='每年发的原创微博被点赞数量统计', data=data)
	# 转发量统计
	data = {}
	for key, value in all_data.items():
		if not value[0]:
			continue
		year = value[1].split('-')[0]
		if year in data:
			data[year] += value[3]
		else:
			data[year] = value[3]
	data = dict(sorted(data.items(), key=lambda i: i[0]))
	drawBar(title='每年发的原创微博被转发数量统计', data=data)
	# 评论量统计
	data = {}
	for key, value in all_data.items():
		if not value[0]:
			continue
		year = value[1].split('-')[0]
		if year in data:
			data[year] += value[4]
		else:
			data[year] = value[4]
	data = dict(sorted(data.items(), key=lambda i: i[0]))
	drawBar(title='每年发的原创微博被评论数量统计', data=data)