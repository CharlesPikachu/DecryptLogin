# Simulated login


## Login class
For users who only want to simply get the login-in session, it is recommended to use the Login class object provided by the DecryptLogin library.
Specifically, here is an example:
```python
from DecryptLogin import login

# the instanced Login class object
lg = login.Login()
# use the provided api function to login in the target website (e.g. twitter)
infos_return, session = lg.twitter(username='Your Username', password='Your Password')
```
All the api functions for logining in the corresponding websites support the following arguments:
```
username: the username for login in the target website
password: the password for login in the target website
mode: pc/mobile, using the default setting is recommended
crackvcFunc: a user-defined captcha identification function, the input of this function is the image path of captcha and it should return the recognition result of captcha
proxies: use proxies during the simulated login, the supported formats of proxies is the same as https://requests.readthedocs.io/en/master/user/advanced/#proxies
```


## Loginer class
The DecryptLogin library also supports returning the instantiated simulated login class of the corresponding website before implementing the simulated login. 
Specifically, the code could be implemented as follows:
```python
from DecryptLogin import login

# the instanced Loginer class object
loginer = login.Loginer()
# obtain the simulated login class of the corresponding website (e.g. twitter)
twitter_loginer = loginer.twitter()
# call login function to achieve simulated login
infos_return, session = twitter_loginer.login(username='Your Username', password='Your Password')
```
The arguments supported by the login function are the same as those used to implement simulated login support using the Login class object.
The advantage of this scheme is that it is easier to call other useful functions in this class in order to achieve functions other than simulated login.


## Introduction of supported websites

### Weibo
#### Supported modes
The supported modes of Weibo include:
- mobile
- pc
#### Example
Here is an example to login in Weibo:
```python
from DecryptLogin import login
lg = login.Login()
# pc
infos_return, session = lg.weibo(username[telephone], password, 'pc')
# mobile
infos_return, session = lg.weibo(username[telephone], password, 'mobile')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### Douban
#### Supported modes
The supported modes of Douban include:
- pc
#### Example
Here is an example to login in Douban:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.douban(username[telephone], password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Github
#### Supported modes
The supported modes of Github include:
- pc
#### Example
Here is an example to login in Github:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.github(username[email], password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Music163
#### Supported modes
The supported modes of Music163 include:
- pc
#### Example
Here is an example to login in Music163:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.music163(username[telephone/email], password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Zt12306
#### Supported modes
The supported modes of Zt12306 include:
- pc
#### Example
Here is an example to login in Zt12306:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zt12306(username[telephone], password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a click captcha, just return the index of target images (e.g., return '1,6' means the target images are in <the first row, the first column> and <the second row, the second column>)

### QQZone
#### Supported modes
The supported modes of QQZone include:
- pc
#### Example
Here is an example to login in QQZone:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in QQZone
infos_return, session = lg.QQZone('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### QQQun
#### Supported modes
The supported modes of QQQun include:
- pc
#### Example
Here is an example to login in QQQun:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in QQQun
infos_return, session = lg.QQQun('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### QQId
#### Supported modes
The supported modes of QQId include:
- pc
#### Example
Here is an example to login in QQId:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in QQId
infos_return, session = lg.QQId('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Zhihu
#### Supported modes
The supported modes of Zhihu include:
- pc
#### Example
Here is an example to login in Zhihu:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zhihu(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### Bilibili
#### Supported modes
The supported modes of Bilibili include:
- mobile
- pc
#### Example
Here is an example to login in Bilibili:
```python
from DecryptLogin import login
lg = login.Login()
# pc
infos_return, session = lg.bilibili(username, password, 'pc')
# mobile
infos_return, session = lg.bilibili(username, password, 'mobile')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha, use the recognition api from https://github.com/Hsury/Bilibili-Toolkit
- pc: unsupport processing the situation of appearing captcha, use the recognition api from https://github.com/Hsury/Bilibili-Toolkit

### Toutiao
#### Supported modes
The supported modes of Toutiao include:
- mobile
#### Example
Here is an example to login in Toutiao:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.toutiao(username, password, 'mobile')
```
#### The returned values in crackvcFunc
- mobile: it is a digital captcha, just return the corresponding digital recognition result
- pc: unsupport processing the situation of appearing captcha

### Taobao
#### Supported modes
The supported modes of Taobao include:
- pc
#### Example
Here is an example to login in Taobao:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in taobao
infos_return, session = lg.taobao('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Jingdong
#### Supported modes
The supported modes of Jingdong include:
- pc
#### Example
Here is an example to login in Jingdong:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in jingdong
infos_return, session = lg.jingdong('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Ifeng
#### Supported modes
The supported modes of Ifeng include:
- pc
#### Example
Here is an example to login in Ifeng:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.ifeng(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### Sohu
#### Supported modes
The supported modes of Sohu include:
- mobile
- pc
#### Example
Here is an example to login in Sohu:
```python
from DecryptLogin import login
lg = login.Login()
# pc
infos_return, session = lg.sohu(username, password, 'pc')
# mobile
infos_return, session = lg.sohu(username, password, 'mobile')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Zgconline
#### Supported modes
The supported modes of Zgconline include:
- pc
#### Example
Here is an example to login in Zgconline:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zgconline(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Lagou
#### Supported modes
The supported modes of Lagou include:
- pc
#### Example
Here is an example to login in Lagou:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.lagou(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### Twitter
#### Supported modes
The supported modes of Twitter include:
- pc
#### Example
Here is an example to login in Twitter:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.twitter(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Vultr
#### Supported modes
The supported modes of Vultr include:
- pc
#### Example
Here is an example to login in Vultr:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.vultr(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### eSurfing
#### Supported modes
The supported modes of eSurfing include:
- pc
#### Example
Here is an example to login in eSurfing:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.eSurfing(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Renren
#### Supported modes
The supported modes of Renren include:
- pc
#### Example
Here is an example to login in Renren:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.renren(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### W3Cschool
#### Supported modes
The supported modes of W3Cschool include:
- pc
#### Example
Here is an example to login in W3Cschool:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.w3cschool(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Fishc
#### Supported modes
The supported modes of Fishc include:
- pc
#### Example
Here is an example to login in Fishc:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.fishc(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Youdao
#### Supported modes
The supported modes of Youdao include:
- pc
#### Example
Here is an example to login in Youdao:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.youdao(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Baidupan
#### Supported modes
The supported modes of Baidupan include:
- pc
#### Example
Here is an example to login in Baidupan:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.baidupan(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### Stackoverflow
#### Supported modes
The supported modes of Stackoverflow include:
- pc
#### Example
Here is an example to login in Stackoverflow:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.stackoverflow(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### CodaLab
#### Supported modes
The supported modes of CodaLab include:
- pc
#### Example
Here is an example to login in CodaLab:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.codalab(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### PyPi
#### Supported modes
The supported modes of PyPi include:
- pc
#### Example
Here is an example to login in PyPi:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.pypi(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Xiami
#### Supported modes
The supported modes of Xiami include:
- pc
#### Example
Here is an example to login in Xiami:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.xiami(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Douyu
#### Supported modes
The supported modes of Douyu include:
- pc
#### Example
Here is an example to login in Douyu:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in Douyu
infos_return, session = lg.douyu('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Migu
#### Supported modes
The supported modes of Migu include:
- pc
#### Example
Here is an example to login in Migu:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.migu(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Qunar
#### Supported modes
The supported modes of Qunar include:
- pc
#### Example
Here is an example to login in Qunar:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.qunar(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### Mieshop
#### Supported modes
The supported modes of Mieshop include:
- pc
#### Example
Here is an example to login in Mieshop:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.mieshop(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### Mpweixin
#### Supported modes
The supported modes of Mpweixin include:
- pc
#### Example
Here is an example to login in Mpweixin:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.mpweixin(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha


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