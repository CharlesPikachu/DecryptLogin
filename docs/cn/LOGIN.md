# 模拟登录


## 利用Login类实现模拟登录
对于仅想实现网站模拟登录功能的用户, 推荐使用DecryptLogin库提供的Login类对象。具体而言, 代码实现如下:
```python
from DecryptLogin import login

# 实例化Login类对象
lg = login.Login()
# 调用对应的接口实现模拟登录(以知乎为例)
infos_return, session = lg.zhihu(username='Your Username', password='Your Password')
```
所有网站接口均支持以下几个参数:
```
username: 登录用户名
password: 登录密码
mode: 选择使用移动端(mode='mobile')/PC端接口(mode='pc'), 一般使用默认的接口即可
crackvcFunc: 支持用户自定义一个验证码识别函数, 该函数传入验证码图片路径, 并返回识别结果
proxies: 模拟登录的过程中使用指定的代理服务器, 代理支持的格式同: https://requests.readthedocs.io/en/master/user/advanced/#proxies
```


## 利用Loginer类实现模拟登录
DecryptLogin库也支持先返回对应网站的实例化模拟登录类, 然后再实现模拟登录。具体而言，代码实现如下:
```python
from DecryptLogin import login

# 实例化Loginer类对象
loginer = login.Loginer()
# 获得对应网站的模拟登录类(以知乎为例)
zhihu_loginer = loginer.zhihu()
# 调用login函数实现模拟登录
infos_return, session = zhihu_loginer.login(username='Your Username', password='Your Password')
```
login函数支持的参数与上面利用Login类对象实现模拟登录支持的参数一致。该方案的好处是可以更方便地调用类中其他有用的方法, 以便实现模拟登录以外的功能。


## 各平台模拟登录简介

### 新浪微博
#### 支持的登录mode
新浪微博目前支持的登录mode包括:
- mobile
- pc
#### 示例代码
新浪微博模拟登录的示例代码如下:
```python
from DecryptLogin import login
lg = login.Login()
# PC端
infos_return, session = lg.weibo(username[telephone], password, 'pc')
# 移动端
infos_return, session = lg.weibo(username[telephone], password, 'mobile')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 为数字验证码, 返回对应的数字识别结果即可

### 豆瓣
#### 支持的登录mode
豆瓣目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.douban(username[telephone], password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### Github
#### 支持的登录mode
Github目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.github(username[email], password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 网易云音乐
#### 支持的登录mode
网易云音乐目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.music163(username[telephone/email], password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 中国铁路12306
#### 支持的登录mode
中国铁路12306目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zt12306(username[telephone], password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 为点击验证码, 返回需要点击的目标位置索引字符串即可(例如返回'1,6'代表目标位置在第一行第一列和第二行第二列)

### QQ空间
#### 支持的登录mode
QQ空间目前支持的登录mode包括:
- mobile
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
# 因为使用扫码登录, 无需输入用户名密码
infos_return, session = lg.QQZone('mobile')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### QQ群
#### 支持的登录mode
QQ群目前支持的登录mode包括:
- mobile
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
# 因为使用扫码登录, 无需输入用户名密码
infos_return, session = lg.QQQun('mobile')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 我的QQ中心
#### 支持的登录mode
我的QQ中心目前支持的登录mode包括:
- mobile
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
# 因为使用扫码登录, 无需输入用户名密码
infos_return, session = lg.QQId('mobile')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 知乎
#### 支持的登录mode
知乎目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zhihu(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 为数字验证码, 返回对应的数字识别结果即可

### B站
#### 支持的登录mode
B站目前支持的登录mode包括:
- mobile
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
# PC端
infos_return, session = lg.bilibili(username, password, 'pc')
# 移动端
infos_return, session = lg.bilibili(username, password, 'mobile')
```
#### 验证码识别结果格式
- mobile: 暂不支持, 直接调用了https://github.com/Hsury/Bilibili-Toolkit作者提供的接口进行验证码识别
- pc: 暂不支持, 直接调用了https://github.com/Hsury/Bilibili-Toolkit作者提供的接口进行验证码识别

### 今日头条
#### 支持的登录mode
今日头条目前支持的登录mode包括:
- mobile
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.toutiao(username, password, 'mobile')
```
#### 验证码识别结果格式
- mobile: 为数字验证码, 返回对应的数字识别结果即可
- pc: 暂不支持登录时需要验证码的情况处理

### 淘宝
#### 支持的登录mode
淘宝目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
# 因为使用扫码登录, 无需输入用户名密码
infos_return, session = lg.taobao('pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 京东
#### 支持的登录mode
京东目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
# 因为使用扫码登录, 无需输入用户名密码
infos_return, session = lg.jingdong('pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 凤凰网
#### 支持的登录mode
凤凰网目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.ifeng(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 为数字验证码, 返回对应的数字识别结果即可

### 搜狐
#### 支持的登录mode
搜狐目前支持的登录mode包括:
- mobile
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
# PC端
infos_return, session = lg.sohu(username, password, 'pc')
# 移动端
infos_return, session = lg.sohu(username, password, 'mobile')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 中关村在线
#### 支持的登录mode
中关村在线目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.zgconline(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 拉勾网
#### 支持的登录mode
拉勾网目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.lagou(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 为数字验证码, 返回对应的数字识别结果即可

### 推特 
#### 支持的登录mode
推特目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.twitter(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### Vultr
#### 支持的登录mode
Vultr目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.vultr(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 对于无法访问谷歌的用户, Vultr使用数字验证码, 返回对应的数字识别结果即可; 对于可以访问谷歌的用户, Vultr使用谷歌的点击验证码, 暂不支持出现该种验证码时的情况处理

### 天翼
#### 支持的登录mode
天翼目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.eSurfing(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 人人网
#### 支持的登录mode
人人网目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.renren(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 为数字验证码, 返回对应的数字识别结果即可

### W3Cschool(编程狮)
#### 支持的登录mode
W3Cschool(编程狮)目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.w3cschool(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 鱼C论坛
#### 支持的登录mode
鱼C论坛目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.fishc(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 有道
#### 支持的登录mode
有道目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.youdao(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### 百度网盘
#### 支持的登录mode
百度网盘目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.baidupan(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 为数字验证码, 返回对应的数字识别结果即可

### stackoverflow
#### 支持的登录mode
stackoverflow目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.stackoverflow(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### CodaLab
#### 支持的登录mode
CodaLab目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.codalab(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理

### PyPi
#### 支持的登录mode
PyPi目前支持的登录mode包括:
- pc
#### 示例代码
```python
from DecryptLogin import login
lg = login.Login()
infos_return, session = lg.pypi(username, password, 'pc')
```
#### 验证码识别结果格式
- mobile: 暂不支持登录时需要验证码的情况处理
- pc: 暂不支持登录时需要验证码的情况处理


## 一些工具函数

### Cookies
#### Cookies保存
您可以利用如下方法保存登录后的session中的cookies:
```python
from DecryptLogin.utils.cookies import *

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
#### Cookies导入
您可以利用如下方法为requests.Session对象导入cookies:
```python
from DecryptLogin.utils.cookies import *

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