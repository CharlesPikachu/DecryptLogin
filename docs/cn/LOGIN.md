# 模拟登录


## 利用Login类实现模拟登录
对于仅想实现网站模拟登录功能的用户, 推荐使用DecryptLogin库提供的Login类对象。具体而言, 代码实现如下:
```python
from DecryptLogin import login

# 实例化Login类对象
lg = login.Login()
# 调用对应的接口实现模拟登录(以B站为例)
infos_return, session = lg.bilibili(username='Your Username', password='Your Password')
```
所有网站接口均支持以下几个参数:
```
username: 登录用户名
password: 登录密码
mode: 选择使用移动端登录(mode='mobile')/PC端登录(mode='pc')/扫码登录(mode='scanqr'), 一般使用默认的接口即可
crack_captcha_func: 支持用户自定义一个验证码识别函数, 该函数传入验证码图片路径, 并返回识别结果
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
infos_return, session = zhihu_loginer.login(mode='scanqr')
```
loginer.login函数均支持以下几个参数:
```
username: 登录用户名
password: 登录密码
mode: 选择使用移动端登录(mode='mobile')/PC端登录(mode='pc')/扫码登录(mode='scanqr'), 一般使用默认的接口即可
crack_captcha_func: 支持用户自定义一个验证码识别函数, 该函数传入验证码图片路径, 并返回识别结果
proxies: 模拟登录的过程中使用指定的代理服务器, 代理支持的格式同: https://requests.readthedocs.io/en/master/user/advanced/#proxies
```


## 各平台模拟登录简介

### 新浪微博
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### 移动端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo(username, password, 'mobile')
```
暂不支持crack_captcha_func。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.weibo('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 豆瓣
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douban(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### Github
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.github(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 网易云音乐
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.music163(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 中国铁路12306
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zt12306(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的点击验证码, 返回需要点击的目标位置索引字符串即可, 
例如(返回'1,6'代表目标位置在第一行第一列和第二行第二列):
```python
def cracker(imagepath):
    return '1,6'
```
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### QQ空间
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQZone('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### QQ群
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQQun('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 我的QQ中心
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.QQId('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 知乎
#### PC端登录
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
注意，如果提示"为了您的账号安全，请使用短信验证码登录", 可以尝试绑定邮箱后, 利用邮箱作为用户名登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zhihu('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### B站
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'pc')
```
暂不支持crack_captcha_func, 直接调用了https://github.com/Hsury/Bilibili-Toolkit作者提供的接口进行验证码识别。
#### 移动端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.bilibili(username, password, 'mobile')
```
暂不支持crack_captcha_func, 直接调用了https://github.com/Hsury/Bilibili-Toolkit作者提供的接口进行验证码识别。
#### 扫码登录
暂不支持扫码登录。

### 今日头条
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 淘宝
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.taobao('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 京东
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jingdong('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 凤凰网
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.ifeng(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 搜狐
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.sohu(username, password, 'mobile')
```
暂不支持crack_captcha_func。
#### 扫码登录
暂不支持扫码登录。

### 中关村在线
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.zgconline(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 拉勾网
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 推特 
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.twitter(username, password, 'mobile')
```
暂不支持crack_captcha_func。
#### 扫码登录
暂不支持扫码登录。

### Vultr
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.vultr(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
注意, 对于可以访问谷歌的用户, Vultr使用谷歌的点击验证码, 暂不支持出现该种验证码时的情况处理。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 天翼
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.eSurfing(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 人人网
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.renren(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### W3Cschool(编程狮)
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.w3cschool(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 鱼C论坛
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.fishc(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 有道
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.youdao(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 百度网盘
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidupan(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### Stackoverflow
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.stackoverflow(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### CodaLab
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.codalab(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### PyPi
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.pypi(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 虾米音乐
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.xiami(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 斗鱼直播
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.douyu('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 咪咕音乐
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.migu(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 去哪儿旅行
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qunar(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 小米商城
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mieshop(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 微信公众号
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.mpweixin(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 百度贴吧
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidutieba('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 大众点评
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.dazhongdianping('', '', 'scanqr')
```
暂不支持crack_captcha_func。

### 坚果云
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.jianguoyun(username, password, 'pc')
```
暂不支持crack_captcha_func。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### 天翼云盘
#### PC端登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.cloud189(username, password, 'pc')
```
支持用户自定义crack_captcha_func识别PC端登录的数字字母验证码, 例如:
```python
def cracker(imagepath):
    return 'LOVE'
```
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
暂不支持扫码登录。

### QQ音乐
#### PC端登录
暂不支持PC端登录。
#### 移动端登录
暂不支持移动端登录。
#### 扫码登录
示例代码:
```python
from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.qqmusic('', '', 'scanqr')
```
暂不支持crack_captcha_func。


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