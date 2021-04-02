from DecryptLogin import login
from DecryptLogin.crackcaptcha.weibo import recognize_chaptcha
lg = login.Login()
# PC端
# pytorch 深度学习训练的模型 本地自动识别微博验证码
# 为了避免DecryptLogin过大，没有把模型也放在仓库中
# 模型下载地址  https://github.com/skygongque/captcha_crack_demo/releases/download/1.0/ctc_625_22.pth
# 把模型放到 DecryptLogin\crackcaptcha
infos_return, session = lg.weibo('', '', 'pc',crackvcFunc=recognize_chaptcha)
print(infos_return,session)