# DecryptLogin
```
APIs for loginning some websites using <requests>.
You can star this repository to keep track of the project if it's helpful for you, thank you for your support.
```

# Introduction in Chinese
https://mp.weixin.qq.com/s/lctw2dGjOesXrfvkNhzYfQ
#### Some Cases by using DecryptLogin
- weiboMonitor: https://mp.weixin.qq.com/s/uOT1cGqXkOq-Hdc8TVnglg
- QQReport: https://mp.weixin.qq.com/s/dsVtEp_TFeyeSAAUn1zFEw

# Support List
|  Websites        | support PC API?                              |  support mobile API?                       |  in Chinese    |
|  :----:          | :----:                                       |  :----:                                    |  :----:        |
|  weibo           | [Yes](./DecryptLogin/platforms/weibo.py)     |  [Yes](./DecryptLogin/platforms/weibo.py)  |  新浪微博      |
|  douban          | [Yes](./DecryptLogin/platforms/douban.py)    |  No                                        |  豆瓣          |
|  GitHub          | [Yes](./DecryptLogin/platforms/github.py)    |  No                                        |  Github        |
|  Music163        | [Yes](./DecryptLogin/platforms/music163.py)  |  No                                        |  网易云音乐    |
|  12306           | [Yes](./DecryptLogin/platforms/zt12306.py)   |  No                                        |  中国铁路12306 |
|  QQZone          | No                                           |  [Yes](./DecryptLogin/platforms/QQZone.py) |  QQ空间        |
|  QQQun           | No                                           |  [Yes](./DecryptLogin/platforms/QQQun.py)  |  QQ群          |
|  QQId			   | No                                           |  [Yes](./DecryptLogin/platforms/QQId.py)   |  我的QQ中心    |
|  zhihu		   | [Yes](./DecryptLogin/platforms/zhihu.py)     |  No                                        |  知乎          |

# Install
#### Use setup.py
```sh
Step1:
git clone https://github.com/CharlesPikachu/DecryptLogin.git
Step2:
cd DecryptLogin -> run "python setup.py install"
```
#### Use pip
```sh
pip install git+https://github.com/CharlesPikachu/DecryptLogin.git@master
```

# Usage
#### Arguments
```
Specific Loginning Arguments:
--username: your username.
--password: your password.
--version: pc/mobile.
```
#### Examples
```python
from DecryptLogin import login
lg = login.Login()
username, session = lg.douban(username[telephone], password, 'pc')
username, session = lg.github(username[email], password, 'pc')
username, session = lg.weibo(username[telephone], password, 'mobile')
username, session = lg.music163(username[telephone/email], password, 'pc')
username, session = lg.zt12306(username[telephone], password, 'pc')
username, session = lg.QQZone('mobile')
username, session = lg.QQQun('mobile')
username, session = lg.QQId('mobile')
username, session = lg.zhihu(username, password, 'pc')
```

# More
#### WeChat Official Accounts
*Charles_pikachu*  
![img](./pictures/pikachu.jpg)