# 快速开始

## 三行代码实现模拟登录
你可以利用如下三行代码简单地实现支持列表中的任意一个网站的模拟登录操作。以模拟登录知乎为例:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu(username='Your Username', password='Your Password')
```
其中infos_return为一个字典对象, 包含了一些我认为有用的用户登录信息(例如userid等), session为网站模拟登录后的会话。

## 验证码处理
DecryptLogin默认由用户手动输入验证码, 若您想加入验证码自动识别接口, 则需要传入crackvcFunc函数。还是以知乎为例:
```python
from PIL import Image
from DecryptLogin import login

'''定义验证码识别函数'''
def crackvcFunc(imagepath):
    # 打开验证码图片
    img = Image.open(imagepath)
    # 识别验证码图片
    result = IdentifyAPI(img)
    # 返回识别结果(知乎为数字验证码)
    return result

lg = login.Login()
infos_return, session = lg.zhihu(username='Your Username', password='Your Password', crackvcFunc=crackvcFunc)
```

## 添加代理
若您想利用代理服务器来实现网站模拟登录, 则需传入proxies参数。以模拟登录推特为例:
```
from DecryptLogin import login

lg = login.Login()
proxies = {'https': '127.0.0.1:1080'}
infos_return, session = lg.zhihu(username='Your Username', password='Your Password', proxies=proxies)
```
proxies支持的对象格式请参见: [requests设置代理](https://requests.readthedocs.io/en/master/user/advanced/#proxies)

## 保存cookies
为安全起见, DecryptLogin不考虑提供自动保存cookies并每次验证其是否已经过期的功能。对于有需要保存session对象cookies的用户, 
您可以利用如下方法进行保存:
```python
from DecryptLogin.utils.cookies import *

session = requests.Session()
session.get(url)
saveSessionCookies(session=session, cookiespath='PATH to SAVE COOKIES (e.g., cookies.pkl)')
```
对于验证cookies有效性, 实现并不难, 有需要的用户可自行实现。

## 导入cookies
将之前保存的cookies重新导入到一个requests.Session对象, 您可以利用如下方法:
```python
from DecryptLogin.utils.cookies import *

session = requests.Session()
infos_return, session = loadSessionCookies(session=session, cookiespath='COOKIES PATH to be LOADED')
```