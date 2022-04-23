'''
Function:
    其他工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2022-04-23
'''
import os
import imghdr
import shutil
from PIL import Image


'''显示图像'''
def showImage(imagepath):
    img = Image.open(imagepath)
    img.show()
    img.close()


'''移除图像'''
def removeImage(imagepath):
    os.remove(imagepath)


'''保存图像'''
def saveImage(image, imagepath):
    fp = open(imagepath, 'wb')
    fp.write(image)
    fp.close()
    filetype = imghdr.what(imagepath)
    assert filetype in ['jpg', 'jpeg', 'png', 'bmp', 'gif']
    imagepath_correct = f"{'.'.join(imagepath.split('.')[:-1])}.{filetype}"
    shutil.move(imagepath, imagepath_correct)
    return imagepath_correct