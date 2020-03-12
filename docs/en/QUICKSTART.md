# Quick start

## Login a website with three lines of code
You can use the following three lines of code to easily implement a simulated login operation for any 
website in the support list. Take twitter as an example:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username='Your Username', password='Your Password')
```
where infos_return is a dict object, which contains some user information(e.g. userid) that may be useful. The session is a 
requests.Session object which has logined in the target website.

## Deal with captcha
By default, the users have to handle the captcha by themselves. 
If you want to deal with the captcha more smartly, you can define a captcha identification function and pass it into login api:
```python
from PIL import Image
from DecryptLogin import login

'''the captcha identification function'''
def crackvcFunc(imagepath):
    # open captcha
    img = Image.open(imagepath)
    # identify captcha
    result = IdentifyAPI(img)
    # return the identification result
    return result

lg = login.Login()
infos_return, session = lg.zhihu(username='Your Username', password='Your Password', crackvcFunc=crackvcFunc)
```

## Add proxies
If you want to add proxies for the simulated login operation, you can pass the proxies into login api as following example:
```python
from DecryptLogin import login

lg = login.Login()
proxies = {'https': '127.0.0.1:1080'}
infos_return, session = lg.zhihu(username='Your Username', password='Your Password', proxies=proxies)
```
where the format of proxies is the same as [proxies for requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies)

## Save cookies
You can save the session cookies as following example:
```python
from DecryptLogin.utils.cookies import *

session = requests.Session()
session.get(url)
saveSessionCookies(session=session, cookiespath='PATH to SAVE COOKIES (e.g., cookies.pkl)')
```

## Load cookies
You can load the cookies into a requests.Session as following example:
```python
from DecryptLogin.utils.cookies import *

session = requests.Session()
infos_return, session = loadSessionCookies(session=session, cookiespath='COOKIES PATH to be LOADED')
```