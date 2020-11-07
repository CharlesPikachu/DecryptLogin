# Simulated login


## Login class
For users who only want to simply get the login-in session, it is recommended to use the Login class object provided by the DecryptLogin library.
Specifically, here is an example:
```python
from DecryptLogin import login

# the instanced Login class object
lg = login.Login()
# use the provided api function to login in the target website (e.g., twitter)
infos_return, session = lg.twitter(username='Your Username', password='Your Password')
```
All the api functions for logining in the corresponding websites support the following arguments:
```
username: the username for login in the target website
password: the password for login in the target website
mode: pc/mobile/scanqr, using the default setting is recommended
crack_captcha_func: a user-defined captcha identification function, the input of this function is the image path of captcha and it should return the recognition result of captcha
proxies: use proxies during the simulated login, the supported formats of proxies is the same as https://requests.readthedocs.io/en/master/user/advanced/#proxies
```


## Loginer class
The DecryptLogin library also supports returning the instanced simulated login class of the corresponding website before implementing the simulated login. 
Specifically, the code could be implemented as follows:
```python
from DecryptLogin import login

# the instanced Loginer class object
loginer = login.Loginer()
# obtain the instanced simulated login class of the corresponding website (e.g., twitter)
twitter_loginer = loginer.twitter()
# call login function to achieve simulated login
infos_return, session = twitter_loginer.login(username='Your Username', password='Your Password')
```
All the loginer.login functions for logining in the corresponding websites support the following arguments:
```
username: the username for login in the target website
password: the password for login in the target website
mode: pc/mobile/scanqr, using the default setting is recommended
crack_captcha_func: a user-defined captcha identification function, the input of this function is the image path of captcha and it should return the recognition result of captcha
proxies: use proxies during the simulated login, the supported formats of proxies is the same as https://requests.readthedocs.io/en/master/user/advanced/#proxies
```


## Introduction of supported websites

### Weibo
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### Mobile Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'mobile')
```
Unsupport the user-defined crack_captcha_func.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Douban
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douban(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Github
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.github(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Music163
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.music163(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Zt12306
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zt12306(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the click captcha automatically, 
for example (return '1,6' means the image need to be selected is in [the first row, the first column] and [the second row, the second column]):
```python
def cracker(imagepath):
    return '1,6'
```
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### QQZone
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQZone('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### QQQun
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQQun('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### QQId
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQId('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Zhihu
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
Noted that, email is recommended as the input of username.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Bilibili
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func, we use the recognition api from https://github.com/Hsury/Bilibili-Toolkit.
#### Mobile Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'mobile')
```
Unsupport the user-defined crack_captcha_func, we use the recognition api from https://github.com/Hsury/Bilibili-Toolkit.
#### Scanqr Mode
This mode is temporarily not supported.

### Toutiao
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Taobao
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.taobao('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Jingdong
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jingdong('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Ifeng
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.ifeng(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Sohu
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.sohu(username, password, 'mobile')
```
Unsupport the user-defined crack_captcha_func.
#### Scanqr Mode
This mode is temporarily not supported.

### Zgconline
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zgconline(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Lagou
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Twitter
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Vultr
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.vultr(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
Noted that Vultr will adopt the google's click captcha when your network could access google. However, crack_captcha_func only support crack the digital/letter captcha.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### eSurfing
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.eSurfing(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Renren
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.renren(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### W3Cschool
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.w3cschool(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Fishc
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.fishc(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Youdao
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.youdao(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Baidupan
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidupan(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Stackoverflow
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.stackoverflow(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### CodaLab
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.codalab(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### PyPi
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.pypi(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Xiami
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.xiami(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Douyu
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douyu('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Migu
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.migu(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Qunar
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qunar(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Mieshop
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mieshop(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Mpweixin
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mpweixin(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Baidutieba
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidutieba('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Dazhongdianping
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.dazhongdianping('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.

### Jianguoyun
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jianguoyun(username, password, 'pc')
```
Unsupport the user-defined crack_captcha_func.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### Cloud189
#### PC Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.cloud189(username, password, 'pc')
```
Support the user-defined crack_captcha_func to identify the digital/letter captcha automatically, for example:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
This mode is temporarily not supported.

### QQMusic
#### PC Mode
This mode is temporarily not supported.
#### Mobile Mode
This mode is temporarily not supported.
#### Scanqr Mode
The sample code is as following:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qqmusic('', '', 'scanqr')
```
Unsupport the user-defined crack_captcha_func.


## Util functions

### cookies
#### save cookies
You can save the cookies in requests.Session as follows:
```python
from DecryptLogin.utils.cookies import *

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
#### load cookies
You can load the saved cookies into requests.Session as follows:
```python
from DecryptLogin.utils.cookies import *

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