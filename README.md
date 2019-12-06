# DecryptLogin
```
APIs for loginning some websites using <requests>.
You can star this repository to keep track of the project if it's helpful for you, thank you for your support.
```

# Introduction in Chinese
https://mp.weixin.qq.com/s/lctw2dGjOesXrfvkNhzYfQ
#### Some Examples
- weiboMonitor: https://mp.weixin.qq.com/s/uOT1cGqXkOq-Hdc8TVnglg

# Done
#### weibo
- [ ] PC
- [x] [mobile](https://m.weibo.cn/) → in src/platforms/weibo.py
#### douban
- [x] [PC](https://www.douban.com/) → in src/platforms/douban.py
- [ ] mobile
#### QQ zone
- [ ] PC
- [x] [mobile](https://ssl.ptlogin2.qq.com/ptqrlogin) → in src/platforms/QQZone.py
#### GitHub
- [x] [PC](https://github.com/) → in src/platforms/github.py
- [ ] mobile
#### Music163
- [x] [PC](https://music.163.com/) → in src/platforms/music163.py
- [ ] mobile
#### 12306
- [x] [PC](https://www.12306.cn/index/) → in src/platforms/zt12306.py
- [ ] mobile

# Install
### Use setup.py
#### Step1
```sh
git clone https://github.com/CharlesPikachu/DecryptLogin.git
```
#### Step2
```sh
cd DecryptLogin -> run "python setup.py install"
```
### Use pip
```sh
pip install git+https://github.com/CharlesPikachu/DecryptLogin.git@master
```

# Usage
#### Example
```python
from DecryptLogin import login
l = login.Login()
session = l.douban(username[telephone], password, 'pc')
session = l.github(username[email], password, 'pc')
session = l.weibo(username[telephone], password, 'mobile')
session = l.music163(username[telephone/email], password, 'pc')
session = l.zt12306(username[telephone], password, 'pc')
session = l.QQZone('mobile')
```
#### Explain
```
username: your username.
password: your password.
version: pc/mobile.
```

# More
#### WeChat Official Accounts
*Charles_pikachu*  
![img](./pictures/pikachu.jpg)