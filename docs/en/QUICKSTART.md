# Quick Start


#### Login in a website with three lines of code

You can use the following three lines of code to easily implement a simulated login operation for any 
website in the support list. Take twitter as an example:

```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username='Your Username', password='Your Password')
```

where infos_return is a dict object, which contains some user information(e.g., userid) that may be useful. The session is a 
requests.Session object which has logined in the target website. Here is a screenshot:

<div align="center">
    <img src="https://raw.githubusercontent.com/CharlesPikachu/DecryptLogin/master/docs/login.gif" width="600"/>
</div>
<br />


#### Login in a website with login.Client

You can also login in the website by leveraging login.Client:

```sh
from DecryptLogin import login

client = login.Client()
weibo = client.weibo(reload_history=True)
infos_return, session = weibo.login('me', 'pass', mode='scanqr')
```

"reload_history=True" is used to reload the corresponding historical session saved in the computer and check whether the historical session is expired. 
If the historical session is expired, we will start a new login operation.
Here is a screenshot:

<div align="center">
    <img src="https://raw.githubusercontent.com/CharlesPikachu/DecryptLogin/master/docs/login.gif" width="600"/>
</div>
<br />


#### Deal with captcha

By default, the users have to enter the captcha manually. 
If you want to deal with the captcha automatically, you can define a captcha identification function and pass it into the corresponding login api. Here is an example:

```python
from PIL import Image
from DecryptLogin import login

'''the captcha identification function'''
def cracker(imagepath):
    # open captcha
    img = Image.open(imagepath)
    # identify captcha
    result = IdentifyAPI(img)
    # return the identification result
    return result

lg = login.Login()
infos_return, session = lg.baidupan(username='Your Username', password='Your Password', crack_captcha_func=cracker)
```


#### Add proxies

If you want to add proxies for the simulated login operation, you can pass the proxies into the corresponding login api as the following example:

```python
from DecryptLogin import login

lg = login.Login()
proxies = {'https': '127.0.0.1:1080'}
infos_return, session = lg.bilibili(username='Your Username', password='Your Password', proxies=proxies)
```

where the format of proxies is the same as [proxies for requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies).


#### Save cookies

You can save the session cookies as the following example:

```python
from DecryptLogin.modules.utils.cookies import saveSessionCookies

session = requests.Session()
session.get(url)
saveSessionCookies(session=session, cookiespath='PATH to SAVE COOKIES (e.g., cookies.pkl)')
```

#### Load cookies

You can load the cookies into a requests.Session as the following example:

```python
from DecryptLogin.modules.utils.cookies import loadSessionCookies

session = requests.Session()
infos_return, session = loadSessionCookies(session=session, cookiespath='COOKIES PATH to be LOADED')
```