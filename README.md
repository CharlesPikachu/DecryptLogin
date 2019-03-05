# DecryptLogin
```sh
Login some website using requests.
You can star this repository to keep track of the project if it's helpful for you, thank you for your support.
```

# Done
#### weibo
- [ ] PC
- [x] [mobile](https://m.weibo.cn/) → in src/platforms/weibo.py
#### douban
- [x] [PC](https://www.douban.com/) → in src/platforms/douban.py
- [ ] mobile
#### QQ zone
- [ ] PC
- [ ] mobile
#### GitHub
- [x] [PC](https://github.com/) → in src/platforms/github.py
- [ ] mobile
#### WeChat
- [ ] PC
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
### Use install
```sh
pip install git+https://github.com/CharlesPikachu/DecryptLogin.git@master
```

# Usage
#### Example
```sh
from DecryptLogin import login
l = login.Login()
session = l.douban(username[telephone number], password, 'pc')
session = l.github(username[email], password, 'pc')
session = l.weibo(username[telephone number], password, 'mobile')
```
#### Explain
```sh
username: your username.
password: your password.
version: pc/mobile.
```

# More
#### WeChat Official Accounts
*Charles_pikachu*  
![img](./pictures/pikachu.jpg)