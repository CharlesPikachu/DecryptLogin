# Simulated Login


## login.Login

For users who only want to simply obtain the login-in session, it is recommended to use login.Login.
Specifically, here is an example:

```python
from DecryptLogin import login

# the instanced Login class object
lg = login.Login()
# use the provided api function to login in the target website (e.g., twitter)
infos_return, session = lg.twitter(username='Your Username', password='Your Password')
```

The api functions for logining in the corresponding websites all support the following arguments:

- username: the username for login in the target website,
- password: the password for login in the target website,
- mode: pc/mobile/scanqr, using the default setting is recommended,
- crack_captcha_func: a user-defined captcha identification function, the input of this function is the image path of captcha and it should return the recognition result of captcha,
- proxies: use proxies during the simulated login, the supported formats of proxies is the same as [Requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies).


## login.Client

login.Client leverages the instanced website client to perform logining operation.
Specifically, the codes could be implemented as follows:

```python
from DecryptLogin import login

# the instanced client
client = login.Client()
# the instanced weibo
weibo = client.weibo(reload_history=True)
# use the login function to login in weibo
infos_return, session = weibo.login('me', 'pass', 'scanqr')
```

The instanced websites all support the following arguments:

- reload_history: whether try to reload the corresponding historical session saved in the computer.

The login functions for logining in the corresponding websites all support the following arguments:

- username: the username for login in the target website,
- password: the password for login in the target website,
- mode: pc/mobile/scanqr, using the default setting is recommended,
- crack_captcha_func: a user-defined captcha identification function, the input of this function is the image path of captcha and it should return the recognition result of captcha,
- proxies: use proxies during the simulated login, the supported formats of proxies is the same as [Requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies).


## Supported Websites

#### weibo

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported since the sms code is always required when you want to login in PC Mode.

**2.Mobile Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'mobile')
```

The user-defined crack_captcha_func has not been supported since the sms code is always required when you want to login in Mobile Mode.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo('', '', 'scanqr')
```

Then, you can leverage the APP of weibo to scan the qr code to login in the website.

#### douban

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douban(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douban('', '', 'scanqr')
```

Then, you can leverage the APP of douban to scan the qr code to login in the website.

#### github

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.github(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### music163

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.music163(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.music163('', '', 'scanqr')
```

Then, you can leverage the APP of music163 to scan the qr code to login in the website.

#### zt12306

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zt12306(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported since the sms code is always required when you want to login in PC Mode.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zt12306('', '', 'scanqr')
```

Then, you can leverage the APP of zt12306 to scan the qr code to login in the website.

#### QQZone

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQZone('', '', 'scanqr')
```

Then, you can leverage the APP of TIM or QQ to scan the qr code to login in the website.

#### QQQun

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQQun('', '', 'scanqr')
```

Then, you can leverage the APP of TIM or QQ to scan the qr code to login in the website.

#### QQId

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQId('', '', 'scanqr')
```

Then, you can leverage the APP of TIM or QQ to scan the qr code to login in the website.

#### zhihu

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

The mail is recommended to be as the username.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu('', '', 'scanqr')
```

Then, you can leverage the APP of zhihu to scan the qr code to login in the website.

#### bilibili

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported since the sms code is always required when you want to login in PC Mode.

**2.Mobile Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'mobile')
```

The user-defined crack_captcha_func has not been supported since the sms code is always required when you want to login in Mobile Mode.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili('', '', 'scanqr')
```

Then, you can leverage the APP of bilibili to scan the qr code to login in the website.

#### toutiao

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.toutiao('', '', 'scanqr')
```

Then, you can leverage the APP of toutiao to scan the qr code to login in the website.

#### taobao

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.taobao('', '', 'scanqr')
```

Then, you can leverage the APP of taobao to scan the qr code to login in the website.

#### jingdong

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jingdong('', '', 'scanqr')
```

Then, you can leverage the APP of jingdong to scan the qr code to login in the website.

#### ifeng

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.ifeng(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### sohu

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.sohu(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.sohu(username, password, 'mobile')
```

The user-defined crack_captcha_func has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### zgconline

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zgconline(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### lagou

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.lagou(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### twitter 

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username, password, 'mobile')
```

The user-defined crack_captcha_func has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### eSurfing

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.eSurfing('', '', 'scanqr')
```

Then, you can leverage the APP of eSurfing to scan the qr code to login in the website.

#### renren

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.renren(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### w3cschool

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.w3cschool(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### fishc

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.fishc(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### youdao

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.youdao(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### baidupan

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidupan(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

The sms code is always required for secondary verification when you want to login in PC Mode due to the security mechanism.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### stackoverflow

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.stackoverflow(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### codalab

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.codalab(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### pypi

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.pypi(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### douyu

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douyu('', '', 'scanqr')
```

Then, you can leverage the APP of douyu, TIM or QQ to scan the qr code to login in the website.

#### migu

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.migu(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### qunar

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qunar(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### mieshop

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mieshop(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### mpweixin

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mpweixin(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported since the qr code scanned by wechat is always required for the secondary verification when you want to login in PC Mode.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### baidutieba

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidutieba('', '', 'scanqr')
```

Then, you can leverage the APP of baidutieba to scan the qr code to login in the website.

#### dazhongdianping

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.dazhongdianping('', '', 'scanqr')
```

Then, you can leverage the APP of dazhongdianping to scan the qr code to login in the website.

#### jianguoyun

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jianguoyun(username, password, 'pc')
```

The user-defined crack_captcha_func has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### cloud189

**1.PC Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.cloud189(username, password, 'pc')
```

The crack_captcha_func can be defined as follow:

```python
def cracker(imagepath):
    return 'LOVE'
```

**2.Mobile Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.cloud189(username, password, 'mobile')
```

The user-defined crack_captcha_func has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### qqmusic

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qqmusic('', '', 'scanqr')
```

Then, you can leverage the APP of QQ or TIM to scan the qr code to login in the website.

#### ximalaya

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.ximalaya('', '', 'scanqr')
```

Then, you can leverage the APP of ximalaya to scan the qr code to login in the website.

#### icourse163

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.icourse163(username, password, 'mobile')
```

The user-defined crack_captcha_func has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### xiaomihealth

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.xiaomihealth(username, password, 'mobile')
```

The user-defined crack_captcha_func has not been supported.

**3.Scanqr Mode**

The scanqr mode has not been supported.

#### tencentvideo

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.tencentvideo('', '', 'scanqr')
```

Then, you can leverage the APP of QQ or TIM to scan the qr code to login in the website.

#### baidu

**1.PC Mode**

The pc mode has not been supported.

**2.Mobile Mode**

The mobile mode has not been supported.

**3.Scanqr Mode**

The sample codes is as follow::

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidu('', '', 'scanqr')
```

Then, you can leverage the APP of baidu to scan the qr code to login in the website.


## Utility Functions

#### Cookies

**1.Save cookies**

You can save the session cookies as the following example:

```python
from DecryptLogin.modules.utils.cookies import saveSessionCookies

session = requests.Session()
session.get(url)
infos_return = saveSessionCookies(session=session, cookiespath='PATH to SAVE COOKIES (e.g., cookies.pkl)')
```

The explanation of the arguments:

```
Function:
	save the cookies in requests.Session
Input:
	--session: the requests.Session object
	--cookiespath: the file path to save cookies
	--encoding: the encoding of the file for saving cookies
Return:
	--infos_return: return the flag of whether save the cookies successfully, if fail to save, also return the detailed error information
```

**2.Load cookies**

You can load the cookies into a requests.Session as the following example:

```python
from DecryptLogin.modules.utils.cookies import loadSessionCookies

session = requests.Session()
infos_return, session = loadSessionCookies(session=session, cookiespath='COOKIES PATH to be LOADED')
```

The explanation of the arguments:

```
Function:
	load the cookies into requests.Session
Input:
	--session: the requests.Session object before loading cookies
	--cookiespath: the file path of the saved cookies
	--encoding: the encoding of the cookies file
Return:
	--infos_return: return the flag of whether load the cookies successfully, if fail to load, also return the detailed error information
	--session: the requests.Session object after loading cookies
```