from DecryptLogin import login
from DecryptLogin.core.ximalaya import ximalayaCaptchafun
""" 
增加喜马拉雅的pc端登录方式，利用opencv-python通过滑块验证成率在60-70%左右
"""


t = login.ximalaya()
infos_return, session = t.login(username='13512341234',password='123456',mode='pc',crack_captcha_func=ximalayaCaptchafun)
print(infos_return)
print(session.cookies)


