'''
Function:
	其他工具函数
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-04-12
'''
import os
import sys
import subprocess


'''用于在不同OS显示验证码'''
def showImage(img_path):
	try:
		if sys.platform.find('darwin') >= 0: subprocess.call(['open', img_path])
		elif sys.platform.find('linux') >= 0: subprocess.call(['xdg-open', img_path])
		else: os.startfile(img_path)
	except:
		from PIL import Image
		img = Image.open(img_path)
		img.show()
		img.close()


'''验证码验证完毕后关闭验证码并移除'''
def removeImage(img_path):
	if sys.platform.find('darwin') >= 0:
		os.system("osascript -e 'quit app \"Preview\"'")
	os.remove(img_path)


'''保存验证码图像'''
def saveImage(img, img_path):
	if os.path.isfile(img_path):
		os.remove(img_path)
	fp = open(img_path, 'wb')
	fp.write(img)
	fp.close()