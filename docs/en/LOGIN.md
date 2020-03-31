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

### weibo
#### Supported modes
The supported modes of weibo include:
- mobile
- pc
#### Example
Here is an example to login in weibo:
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

### douban
#### Supported modes
The supported modes of douban include:
- pc
#### Example
Here is an example to login in douban:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.douban(username[telephone], password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### github
#### Supported modes
The supported modes of github include:
- pc
#### Example
Here is an example to login in github:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.github(username[email], password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### music163
#### Supported modes
The supported modes of music163 include:
- pc
#### Example
Here is an example to login in music163:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.music163(username[telephone/email], password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### zt12306
#### Supported modes
The supported modes of zt12306 include:
- pc
#### Example
Here is an example to login in zt12306:
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
- mobile
#### Example
Here is an example to login in QQZone:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in QQZone
infos_return, session = lg.QQZone('mobile')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### QQQun
#### Supported modes
The supported modes of QQQun include:
- mobile
#### Example
Here is an example to login in QQQun:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in QQQun
infos_return, session = lg.QQQun('mobile')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### QQId
#### Supported modes
The supported modes of QQId include:
- mobile
#### Example
Here is an example to login in QQId:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in QQId
infos_return, session = lg.QQId('mobile')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### zhihu
#### Supported modes
The supported modes of zhihu include:
- pc
#### Example
Here is an example to login in zhihu:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zhihu(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### bilibili
#### Supported modes
The supported modes of bilibili include:
- mobile
- pc
#### Example
Here is an example to login in bilibili:
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

### toutiao
#### Supported modes
The supported modes of toutiao include:
- mobile
#### Example
Here is an example to login in toutiao:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.toutiao(username, password, 'mobile')
```
#### The returned values in crackvcFunc
- mobile: it is a digital captcha, just return the corresponding digital recognition result
- pc: unsupport processing the situation of appearing captcha

### taobao
#### Supported modes
The supported modes of taobao include:
- pc
#### Example
Here is an example to login in taobao:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in taobao
infos_return, session = lg.taobao('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### jingdong
#### Supported modes
The supported modes of jingdong include:
- pc
#### Example
Here is an example to login in jingdong:
```python
from DecryptLogin import login
lg = login.Login()
# scan the qr code to login in jingdong
infos_return, session = lg.jingdong('pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### ifeng
#### Supported modes
The supported modes of ifeng include:
- pc
#### Example
Here is an example to login in ifeng:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.ifeng(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### sohu
#### Supported modes
The supported modes of sohu include:
- mobile
- pc
#### Example
Here is an example to login in sohu:
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

### zgconline
#### Supported modes
The supported modes of zgconline include:
- pc
#### Example
Here is an example to login in zgconline:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zgconline(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### lagou
#### Supported modes
The supported modes of lagou include:
- pc
#### Example
Here is an example to login in lagou:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.lagou(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### twitter
#### Supported modes
The supported modes of twitter include:
- pc
#### Example
Here is an example to login in twitter:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.twitter(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### vultr
#### Supported modes
The supported modes of vultr include:
- pc
#### Example
Here is an example to login in vultr:
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

### renren
#### Supported modes
The supported modes of renren include:
- pc
#### Example
Here is an example to login in renren:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.renren(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### w3cschool
#### Supported modes
The supported modes of w3cschool include:
- pc
#### Example
Here is an example to login in w3cschool:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.w3cschool(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### fishc
#### Supported modes
The supported modes of fishc include:
- pc
#### Example
Here is an example to login in fishc:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.fishc(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### youdao
#### Supported modes
The supported modes of youdao include:
- pc
#### Example
Here is an example to login in youdao:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.youdao(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: unsupport processing the situation of appearing captcha

### baidupan
#### Supported modes
The supported modes of baidupan include:
- pc
#### Example
Here is an example to login in baidupan:
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.baidupan(username, password, 'pc')
```
#### The returned values in crackvcFunc
- mobile: unsupport processing the situation of appearing captcha
- pc: it is a digital captcha, just return the corresponding digital recognition result

### stackoverflow
#### Supported modes
The supported modes of stackoverflow include:
- pc
#### Example
Here is an example to login in stackoverflow:
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