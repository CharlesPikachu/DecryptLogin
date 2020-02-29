'''
Function:
	定义一些工具函数
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import pickle
from wordcloud import WordCloud
from PIL import Image, ImageDraw, ImageFont


'''以.pkl格式保存数据'''
def saveData2Pkl(data, savepath):
	with open(savepath, 'wb') as f:
		pickle.dump(data, f)
	return True


'''导出.pkl格式数据'''
def loadPkl(filepath):
	with open(filepath, 'rb') as f:
		data = pickle.load(f)
	return data


'''检测文件夹是否存在'''
def checkDir(dirpath):
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
		return False
	return True


'''利用个人基本信息制作QQ个人名片'''
def makePersonalCard(personal_info, bgpath, color=(0, 0, 0), fontpath=None, fontsize=50, savepath=None):
	font = ImageFont.truetype(fontpath, fontsize)
	num = len(personal_info.keys())
	img = Image.open(bgpath)
	width, height = img.width, img.height
	draw = ImageDraw.Draw(img)
	interval = (height - num * fontsize) // (num + 1)
	x = 20
	y = interval * 3
	for key, value in personal_info.items():
		if key == '个性签名':
			draw.text((x, y), '%s: ' % key, color, font)
			y += interval
			draw.text((x, y), '%s' % value, color, font)
			y += interval
		else:
			draw.text((x, y), '%s: %s' % (key, value), color, font)
			y += interval
	img.save(savepath)


'''词云'''
def drawWordCloud(words, savepath=None, font_path=None):
	wc = WordCloud(font_path=font_path, background_color='white', max_words=2000, width=1920, height=1080, margin=5)
	wc.generate_from_frequencies(words)
	wc.to_file(savepath)


'''最近的操作名片'''
def makeRecentCard(friends_info, recent_operation_info, bgpath, color=(0, 0, 0), fontpath=None, fontsize=50, savepath=None):
	font = ImageFont.truetype(fontpath, fontsize)
	img = Image.open(bgpath)
	width, height = img.width, img.height
	draw = ImageDraw.Draw(img)
	interval = (height - 10 * fontsize) // 11
	x = 20
	y = interval * 3
	key = '过去30天我退出的群个数'
	value = recent_operation_info.get(key)
	draw.text((x, y), '%s: %s' % (key, value), color, font)
	y += interval
	key = '过去30天我退出的群'
	value = ','.join(recent_operation_info.get(key))
	draw.text((x, y), '%s: %s' % (key, value), color, font)
	y += interval
	key = '过去一年我删除的好友个数'
	value = recent_operation_info.get(key)
	draw.text((x, y), '%s: %s' % (key, value), color, font)
	y += interval
	key = '过去一年我删除的好友'
	value = ','.join(recent_operation_info.get(key))
	draw.text((x, y), '%s: %s' % (key, value), color, font)
	y += interval * 2
	key1 = '我在意谁'
	key2 = '谁在意我'
	value1 = recent_operation_info.get(key1)
	value2 = recent_operation_info.get(key2)
	x1 = 20
	x2 = width // 2
	draw.text((x1, y), '%s' % key1, color, font)
	draw.text((x2, y), '%s' % key2, color, font)
	y += interval
	for v1, v2 in zip(value1, value2):
		draw.text((x1, y), '%s, 亲密度: %s' % (friends_info[v1[0]][0], v1[1]), color, font)
		draw.text((x2, y), '%s, 亲密度: %s' % (friends_info[v2[0]][0], v2[1]), color, font)
		y += interval
	img.save(savepath)