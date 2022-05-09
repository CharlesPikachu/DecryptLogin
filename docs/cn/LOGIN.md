# 模拟登录


## 利用Login类实现模拟登录

对于仅想实现网站模拟登录功能的用户, 推荐使用DecryptLogin库提供的Login类对象。具体而言, 代码实现如下:

```python
from DecryptLogin import login

# 实例化Login类对象
lg = login.Login()
# 调用对应的接口实现模拟登录(以B站为例)
infos_return, session = lg.bilibili(username='Your Username', password='Your Password')
```

所有网站接口均支持以下几个参数:

- username: 登录用户名;
- password: 登录密码;
- mode: 选择使用移动端登录(mode='mobile')/PC端登录(mode='pc')/扫码登录(mode='scanqr'), 一般使用默认的接口即可;
- crack_captcha_func: 支持用户自定义一个验证码识别函数, 该函数传入验证码图片路径, 并返回识别结果;
- proxies: 模拟登录的过程中使用指定的代理服务器, 代理支持的格式同[Requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies)。


## 利用Client类实现模拟登录

Client类为目标网站的客户端类，集成了目标网站的一些常用加密算法，并支持历史登录状态检测的功能。
换句话说，如果你用DecryptLogin在某个电脑上登录过，则该电脑会把你session保留下来，下次再在该电脑上进行登录操作时，我们会优先导入之前保留的session，并自动检测该session是否已经过期，若过期，则再发起新的登录操作。
具体而言, 代码实现如下:

```python
from DecryptLogin import login

# 实例化Client对象
client = login.Client()
# 实例化微博客户端
weibo = client.weibo(reload_history=True)
# 调用login函数进行模拟登录
infos_return, session = weibo.login('me', 'pass', 'scanqr')
```

所有网站的Client实例化对象均支持以下几个参数：

- reload_history: 是否进行历史登录状态检测，设置为False则直接发起新的模拟登录请求。

所有网站的Login函数均支持以下几个参数:

- username: 登录用户名;
- password: 登录密码;
- mode: 选择使用移动端登录(mode='mobile')/PC端登录(mode='pc')/扫码登录(mode='scanqr'), 一般使用默认的接口即可;
- crack_captcha_func: 支持用户自定义一个验证码识别函数, 该函数传入验证码图片路径, 并返回识别结果;
- proxies: 模拟登录的过程中使用指定的代理服务器, 代理支持的格式同[Requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies)。


## 各平台模拟登录简介

#### 新浪微博

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'pc')
```

暂不支持crack_captcha_func，因为目前微博的PC端登录都需要短信验证码验证，运行之后根据提示输入收到的SMS码即可。

**2.移动端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'mobile')
```

暂不支持crack_captcha_func，因为目前微博的移动端登录都需要短信验证码验证，运行之后根据提示输入收到的SMS码即可。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo('', '', 'scanqr')
```

利用微博APP扫码登录即可。

#### 豆瓣

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douban(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douban('', '', 'scanqr')
```

利用豆瓣APP扫码登录即可。

#### Github

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.github(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 网易云音乐

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.music163(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.music163('', '', 'scanqr')
```

利用网易云音乐的APP扫码登录即可。

#### 中国铁路12306

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zt12306(username, password, 'pc')
```

暂不支持crack_captcha_func，因为目前中国铁路12306的PC端登录都需要短信验证码验证，运行之后根据提示输入收到的SMS码即可。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zt12306('', '', 'scanqr')
```

利用中国铁路12306的APP扫码登录即可。

#### QQ空间

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQZone('', '', 'scanqr')
```

利用TIM或者QQ的APP扫码登录即可。

#### QQ群

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQQun('', '', 'scanqr')
```

利用TIM或者QQ的APP扫码登录即可。

#### 我的QQ中心

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQId('', '', 'scanqr')
```

利用TIM或者QQ的APP扫码登录即可。

#### 知乎

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

注意，如果提示"为了您的账号安全，请使用短信验证码登录", 可以尝试绑定邮箱后, 利用邮箱作为用户名登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu('', '', 'scanqr')
```

利用知乎的APP扫码登录即可。

#### B站

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'pc')
```

暂不支持crack_captcha_func，因为目前B站的PC端登录都需要短信验证码验证，运行之后根据提示输入收到的SMS码即可。

**2.移动端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'mobile')
```

暂不支持crack_captcha_func，因为目前B站的移动端登录都需要短信验证码验证，运行之后根据提示输入收到的SMS码即可。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili('', '', 'scanqr')
```

利用BiliBili的APP扫码登录即可。

#### 今日头条

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.toutiao('', '', 'scanqr')
```

利用今日头条的APP扫码登录即可。

#### 淘宝

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.taobao('', '', 'scanqr')
```

利用淘宝的APP扫码登录即可。

#### 京东

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jingdong('', '', 'scanqr')
```

利用京东的APP扫码登录即可。

#### 凤凰网

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.ifeng(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 搜狐

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.sohu(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.sohu(username, password, 'mobile')
```

暂不支持crack_captcha_func。

**3.扫码登录**

暂不支持扫码登录。

#### 中关村在线

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zgconline(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 拉勾网

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.lagou(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 推特 

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username, password, 'mobile')
```

暂不支持crack_captcha_func。

**3.扫码登录**

暂不支持扫码登录。

#### 天翼

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.eSurfing('', '', 'scanqr')
```

利用天翼的APP扫码登录即可。

#### 人人网

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.renren(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### W3Cschool(编程狮)

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.w3cschool(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 鱼C论坛

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.fishc(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 有道

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.youdao(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 百度网盘

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidupan(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

模拟登录百度网盘一般会触发安全验证机制，请根据提示输入百度网盘账户绑定的手机/邮箱收到的验证码。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### Stackoverflow

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.stackoverflow(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### CodaLab

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.codalab(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### PyPi

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.pypi(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 斗鱼直播

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douyu('', '', 'scanqr')
```

利用斗鱼的APP扫码登录即可，如果你斗鱼账号是和QQ绑定的，也可以用QQ或者TIM扫码登录。

#### 咪咕音乐

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.migu(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 去哪儿旅行

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qunar(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 小米商城

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mieshop(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 微信公众号

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mpweixin(username, password, 'pc')
```

暂不支持crack_captcha_func，密码验证通过后一般需要用微信APP扫码进行二次验证。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 百度贴吧

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidutieba('', '', 'scanqr')
```

使用百度贴吧APP扫码登录即可。

#### 大众点评

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.dazhongdianping('', '', 'scanqr')
```

使用大众点评APP扫码登录即可。

#### 坚果云

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jianguoyun(username, password, 'pc')
```

暂不支持crack_captcha_func。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

暂不支持扫码登录。

#### 天翼云盘

**1.PC端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.cloud189(username, password, 'pc')
```

支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.移动端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.cloud189(username, password, 'mobile')
```

暂不支持crack_captcha_func。

**3.扫码登录**

暂不支持扫码登录。

#### QQ音乐

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qqmusic('', '', 'scanqr')
```

使用QQ或者TIM的APP扫码登录即可。

#### 喜马拉雅

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.ximalaya('', '', 'scanqr')
```

使用喜马拉雅APP扫码登录即可。

#### 中国大学MOOC

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.icourse163(username, password, 'mobile')
```

暂不支持crack_captcha_func。

**3.扫码登录**

暂不支持扫码登录。

#### 小米运动

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.xiaomihealth(username, password, 'mobile')
```

暂不支持crack_captcha_func。

**3.扫码登录**

暂不支持扫码登录。

#### 腾讯视频

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.tencentvideo('', '', 'scanqr')
```

使用QQ或者TIM的APP扫码登录即可。

#### 百度

**1.PC端登录**

暂不支持PC端登录。

**2.移动端登录**

暂不支持移动端登录。

**3.扫码登录**

示例代码:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidu('', '', 'scanqr')
```

使用百度APP扫码登录即可。


## 一些工具函数

#### Cookies

**1.Cookies保存**

您可以利用如下方法保存登录后的session中的cookies:

```python
from DecryptLogin.modules.utils.cookies import saveSessionCookies

session = requests.Session()
session.get(url)
infos_return = saveSessionCookies(session=session, cookiespath='PATH to SAVE COOKIES (e.g., cookies.pkl)')
```

函数参数详解:

```
Function:
	保存requests.Session()的cookies
Input:
	--session: 需要保存cookies的requests.Session()对象
	--cookiespath: cookies的保存路径
	--encoding: 编码方式
Return:
	--infos_return: 是否保存成功的flag, 以及错误原因
```

**2.Cookies导入**

您可以利用如下方法为requests.Session对象导入cookies:

```python
from DecryptLogin.modules.utils.cookies import loadSessionCookies

session = requests.Session()
infos_return, session = loadSessionCookies(session=session, cookiespath='COOKIES PATH to be LOADED')
```

函数参数详解:

```
Function:
	导入cookies到requests.Session()
Input:
	--session: 待导入cookies的requests.Session()对象
	--cookiespath: cookies的保存路径
	--encoding: 编码方式
Return:
	--infos_return: 是否导入成功的flag, 以及错误原因
	--session: 导入cookies之后requests.Session()对象
```