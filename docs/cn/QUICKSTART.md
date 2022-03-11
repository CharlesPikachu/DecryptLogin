# 快速开始


#### 三行代码实现模拟登录

你可以利用如下三行代码简单地实现支持列表中的任意一个网站的模拟登录操作。以模拟登录百度网盘为例:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidupan(username='Your Username', password='Your Password')
```

其中infos_return为一个字典对象, 包含了模拟登录后网站返回的用户登录信息(例如userid等), session为网站模拟登录后的会话。运行效果类似如下：
<div align="center">
    <img src="https://raw.githubusercontent.com/CharlesPikachu/DecryptLogin/master/docs/login.gif" width="600"/>
</div>
<br />


#### 实例化网站Client登录

你也可以通过实例化的网站Client进行登录，例如：

```sh
from DecryptLogin import login

client = login.Client()
weibo = client.weibo(reload_history=True)
infos_return, session = weibo.login('me', 'pass', mode='scanqr')
```

设置"reload_history=True"可以实现历史会话的自动导入功能了，效果类似这样(第一次登录的时候是扫码登录，第二次登录就显示直接导入历史会话了)：
<div align="center">
    <img src="https://raw.githubusercontent.com/CharlesPikachu/DecryptLogin/master/docs/client.gif" width="600"/>
</div>
<br />


#### 验证码处理

DecryptLogin默认由用户手动输入验证码, 若您想加入验证码自动识别接口, 则需要传入crack_captcha_func函数。还是以百度网盘为例:

```python
from PIL import Image
from DecryptLogin import login

'''定义验证码识别函数'''
def cracker(imagepath):
    # 打开验证码图片
    img = Image.open(imagepath)
    # 识别验证码图片
    result = IdentifyAPI(img)
    # 返回识别结果(百度网盘为数字验证码)
    return result

lg = login.Login()
infos_return, session = lg.baidupan(username='Your Username', password='Your Password', crack_captcha_func=cracker)
```


#### 添加代理

若您想利用代理服务器来实现网站模拟登录, 则需传入proxies参数。以模拟登录B站为例:

```
from DecryptLogin import login

lg = login.Login()
proxies = {'https': '127.0.0.1:1080'}
infos_return, session = lg.bilibili(username='Your Username', password='Your Password', proxies=proxies)
```

proxies支持的对象格式请参见: [requests设置代理](https://requests.readthedocs.io/en/master/user/advanced/#proxies)


#### 保存cookies

对于想要保存session对象中的cookies的用户, 您可以利用如下方法进行保存:

```python
from DecryptLogin.modules.utils.cookies import saveSessionCookies

session = requests.Session()
session.get(url)
saveSessionCookies(session=session, cookiespath='PATH to SAVE COOKIES (e.g., cookies.pkl)')
```


#### 导入cookies

将之前保存的cookies重新导入到一个requests.Session对象, 您可以利用如下方法:

```python
from DecryptLogin.modules.utils.cookies import loadSessionCookies

session = requests.Session()
infos_return, session = loadSessionCookies(session=session, cookiespath='COOKIES PATH to be LOADED (e.g., cookies.pkl)')
```