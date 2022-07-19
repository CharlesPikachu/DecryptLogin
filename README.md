<div align="center">
    <img src="./docs/logo.png" width="600"/>
</div>
<br />

[![docs](https://img.shields.io/badge/docs-latest-blue)](https://httpsgithubcomcharlespikachudecryptlogin.readthedocs.io/zh/latest/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/DecryptLogin)](https://pypi.org/project/DecryptLogin/)
[![PyPI](https://img.shields.io/pypi/v/DecryptLogin)](https://pypi.org/project/DecryptLogin)
[![license](https://img.shields.io/github/license/CharlesPikachu/DecryptLogin.svg)](https://github.com/CharlesPikachu/DecryptLogin/blob/master/LICENSE)
[![PyPI - Downloads](https://pepy.tech/badge/DecryptLogin)](https://pypi.org/project/DecryptLogin/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/DecryptLogin?style=flat-square)](https://pypi.org/project/DecryptLogin/)
[![issue resolution](https://isitmaintained.com/badge/resolution/CharlesPikachu/DecryptLogin.svg)](https://github.com/CharlesPikachu/DecryptLogin/issues)
[![open issues](https://isitmaintained.com/badge/open/CharlesPikachu/DecryptLogin.svg)](https://github.com/CharlesPikachu/DecryptLogin/issues)

Documents-CN:  https://httpsgithubcomcharlespikachudecryptlogin.readthedocs.io/zh/latest/

Documents-EN: https://httpsgithubcomcharlespikachudecryptlogin.readthedocs.io/en/latest/


# DecryptLogin

```
APIs for loginning some websites by using requests.
You can star this repository to keep track of the project if it's helpful for you, thank you for your support.
```


# Statements

```
This repo is created for learning python.
If I find that anyone leverage this project in an illegal way, I will delete this project immediately.

本项目仅供python爱好者学习使用, 若作者发现该项目以任何不正当方式被使用, 将立即删除该项目。
希望大家合理利用该项目🙂
```


# Login with Requests

### Install

**Preparation**

- [Nodejs](https://nodejs.org/en/): Since some of the supported websites need to compile the js code, you should install the nodejs in your computer.

**Pip install**

```sh
run "pip install DecryptLogin"
```

**Source code install**

```sh
(1) Offline
Step1: git clone https://github.com/CharlesPikachu/DecryptLogin.git
Step2: cd DecryptLogin -> run "python setup.py install"
(2) Online
run "pip install git+https://github.com/CharlesPikachu/DecryptLogin.git@master"
```

### Support List

|  Website_EN      | PC Mode | Mobile Mode | ScanQR Mode | Website_CN        |
|  :----:          | :----:  | :----:      | :----:      | :----:            |
|  weibo           | ✓       | ✓           | ✓           | 新浪微博          |
|  douban          | ✓       | ✗           | ✓           | 豆瓣              |
|  github          | ✓       | ✗           | ✗           | Github            |
|  music163        | ✓       | ✗           | ✓           | 网易云音乐        |
|  zt12306         | ✓       | ✗           | ✓           | 中国铁路12306     |
|  QQZone          | ✗       | ✗           | ✓           | QQ空间            |
|  QQQun           | ✗       | ✗           | ✓           | QQ群              |
|  QQId            | ✗       | ✗           | ✓           | 我的QQ中心        |
|  zhihu           | ✓       | ✗           | ✓           | 知乎         	 |
|  bilibili        | ✓       | ✓           | ✓           | B站               |
|  toutiao         | ✗       | ✗           | ✓           | 今日头条          |
|  taobao          | ✗       | ✗           | ✓           | 淘宝              |
|  jingdong        | ✗       | ✗           | ✓           | 京东              |
|  ifeng           | ✓       | ✗           | ✗           | 凤凰网            |
|  sohu            | ✓       | ✓           | ✗           | 搜狐              |
|  zgconline       | ✓       | ✗           | ✗           | 中关村在线        |
|  lagou           | ✓       | ✗           | ✗           | 拉勾网            |
|  twitter         | ✓       | ✓           | ✗           | 推特              |
|  eSurfing        | ✗       | ✗           | ✓           | 天翼              |
|  renren          | ✓       | ✗           | ✗           | 人人网            |
|  w3cschool       | ✓       | ✗           | ✗           | W3Cschool(编程狮) |
|  fishc           | ✓       | ✗           | ✗           | 鱼C论坛           |
|  youdao          | ✓       | ✗           | ✗           | 有道              |
|  baidupan        | ✓       | ✗           | ✓           | 百度网盘          |
|  stackoverflow   | ✓       | ✗           | ✗           | Stackoverflow     |
|  codalab         | ✓       | ✗           | ✗           | CodaLab           |
|  pypi            | ✓       | ✗           | ✗           | PyPi              |
|  douyu           | ✗       | ✗           | ✓           | 斗鱼直播          |
|  migu            | ✓       | ✗           | ✗           | 咪咕音乐          |
|  qunar           | ✓       | ✗           | ✗           | 去哪儿旅行        |
|  mieshop         | ✓       | ✗           | ✗           | 小米商城          |
|  mpweixin        | ✓       | ✗           | ✗           | 微信公众号        |
|  baidutieba      | ✗       | ✗           | ✓           | 百度贴吧          |
|  dazhongdianping | ✗       | ✗           | ✓           | 大众点评          |
|  jianguoyun      | ✓       | ✗           | ✗           | 坚果云            |
|  cloud189        | ✓       | ✓           | ✗           | 天翼云盘          |
|  qqmusic         | ✗       | ✗           | ✓           | QQ音乐            |
|  ximalaya        | ✗       | ✗           | ✓           | 喜马拉雅          |
|  icourse163      | ✗       | ✓           | ✗           | 中国大学MOOC      |
|  xiaomihealth    | ✗       | ✓           | ✗           | 小米运动          |
|  tencentvideo    | ✗       | ✗           | ✓           | 腾讯视频          |
|  baidu           | ✗       | ✗           | ✓           | 百度              |
|  alipan          | ✗       | ✗           | ✓           | 阿里云盘          |

### Quick Start

**login.Login**
```python
from DecryptLogin import login

# the instanced Login class object
lg = login.Login()
# use the provided api function to login in the target website (e.g., twitter)
infos_return, session = lg.twitter(username='Your Username', password='Your Password')
```

**login.Client**
```python
from DecryptLogin import login

# the instanced client
client = login.Client()
# the instanced weibo
weibo = client.weibo(reload_history=True)
# use the login function to login in weibo
infos_return, session = weibo.login('me', 'pass', 'scanqr')
```


# Practice with DecryptLogin

### Install

**Preparation**

- [ffmpeg](https://ffmpeg.org/): You should set ffmpeg in environment variable.
- [aria2c](https://aria2.github.io/): You should set aria2c in environment variable.

**Pip install**

```
run "pip install DecryptLoginExamples"
```

### Support List

|  Project_EN                 |   Introduction                                                   |   Core Code                                                                                                                                |  Project_CN                      |
|  :----:                     |   :----:                                                         |   :----:                                                                                                                                   |  :----:                          |
|  weibomonitor               |   [click](https://mp.weixin.qq.com/s/uOT1cGqXkOq-Hdc8TVnglg)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/weibomonitor)                  |  微博监控                        |
|  qqreports                  |	  [click](https://mp.weixin.qq.com/s/dsVtEp_TFeyeSAAUn1zFEw)     |	 [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/qqreports)                     |  生成QQ个人专属报告              |
|  bilibiliuservideos         |   [click](https://mp.weixin.qq.com/s/GaVW4_nbAaO0QvphI7QgnA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/bilibiliuservideos)            |  下载B站指定UP主的所有视频       |
|  neteasesonglistdownloader  |   [click](https://mp.weixin.qq.com/s/_82U7luG6jmV-xb8-Qkiew)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/neteasesonglistdownloader)     |  网易云个人歌单下载器            |
|  neteaselistenleaderboard   |   [click](https://mp.weixin.qq.com/s/Wlf1a82oACc9N7zGezcy8Q)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/neteaselistenleaderboard)      |  网易云个人听歌排行榜            |
|  userweibospider            |   [click](https://mp.weixin.qq.com/s/-3BDTZAE1x7nfCLNq2mFBw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/userweibospider)               |  下载指定微博用户的所有微博数据  |
|  neteasesignin              |   [click](https://mp.weixin.qq.com/s/8d7smUSzW2ds1ypZq-yeFw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/neteasesignin)                 |  网易云音乐自动签到              |
|  weiboemoji                 |   [click](https://mp.weixin.qq.com/s/QiPm4gyE8i5amR5gB3IbBA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/weiboemoji)                    |  微博表情包爬取                  |
|  weibosender                |   [click](https://mp.weixin.qq.com/s/_aIY-iVj3xetfHQyMxflkg)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/weibosender)                   |  大吼一声发微博                  |
|  tbgoods                    |   [click](https://mp.weixin.qq.com/s/NhK9eeWNXv_wPnolccRR-g)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/tbgoods)                       |  淘宝商品数据小爬虫              |
|  jdgoods                    |   [click](https://mp.weixin.qq.com/s/LXheJveR248ZW4SP5F6fjw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/jdgoods)                       |  京东商品数据小爬虫              |
|  delallweibos               |   [click](https://mp.weixin.qq.com/s/E5Erg10FvyutEKaB_JGufA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/delallweibos)                  |  批量删除微博                    |
|  clearqzone                 |   [click](https://mp.weixin.qq.com/s/Fj9MQXXRZ8wuKiX3Tytx8A)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/clearqzone)                    |  批量删除QQ空间说说              |
|  neteaseeveryday            |   [click](https://mp.weixin.qq.com/s/tliFa5CYVEirMEyUj0jPbg)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/neteaseeveryday)               |  在终端看网易云每日歌曲推荐      |
|  neteaseclickplaylist       |   [click](https://mp.weixin.qq.com/s/BpoO55I-jxAGO_Vv32khlA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/neteaseclickplaylist)          |  网易云音乐刷歌曲播放量          |
|  cloud189signin             |   [click](https://mp.weixin.qq.com/s/tSLTSKDMzMAkP2deCjkanA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/cloud189signin)                |  天翼云盘自动签到+抽奖           |
|  moocdl                     |   [click](https://mp.weixin.qq.com/s/KsXU-pMvT8GzpPWVpcWIOA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/moocdl)                        |  中国大学MOOC下载器              |
|  modifymihealthsteps        |   [click](https://mp.weixin.qq.com/s/TQLM9GIW50UWAsKoXb7pzQ)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/modifymihealthsteps)           |  修改小米运动中的步数            |
|  taobaosnap                 |   [click](https://mp.weixin.qq.com/s/vCZYtynHtQAOuQJHvjhpWA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/taobaosnap)                    |  淘宝抢购脚本                    |
|  jingdongsnap               |   [click](https://mp.weixin.qq.com/s/-H8bwuUIPDi41d09tTlvRw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/jingdongsnap)                  |  京东抢购脚本                    |
|  bilibiliupmonitor          |   [click](https://mp.weixin.qq.com/s/KjJLPcqHecK8T8LDVesxJQ)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/bilibiliupmonitor)             |  B站UP主监控                     |
|  bilibililottery            |   [click](https://mp.weixin.qq.com/s/7kGjT48AOG_zB1v-cODgVw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/bilibililottery)               |  B站监控关注的UP主并自动转发抽奖 |
|  weibowater                 |   [click](https://mp.weixin.qq.com/s/Avf169tvDNRLrgmrNj8jUw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/weibowater)                    |  微博水军                        |
|  weiboblacklist             |   [click](https://mp.weixin.qq.com/s/9npyr9banKSUl-mVXYhmPA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/weiboblacklist)                |  微博批量拉黑脚本                |
|  weibolottery               |   [click](https://mp.weixin.qq.com/s/sGT4Pwp-yu2grNvSr3vafQ)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/DecryptLoginExamples/crawlers/weibolottery)                  |  微博自动转发抽奖                |

### Quick Start

```python
from DecryptLoginExamples import client
​
config = {
    'username': 'charlespikachu', 
    'time_interval':  1800,
}
crawler_executor = client.Client()
crawler_executor.executor('bilibililottery', config=config)
```


# Thanks List

|  Author                                            |           Time            |   Contribution                                     |
|  :----:                                            |           :----:          |   :----:                                           |
|  @[skygongque](https://github.com/skygongque)      |           2020-02-13      |   add verification code processing in (weibo, pc)  |


# Citation

If you use this project in your research, please cite this project:

```
@misc{decryptlogin2020,
    author = {Zhenchao Jin},
    title = {DecryptLogin: APIs for loginning some websites by using requests},
    year = {2020},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/CharlesPikachu/DecryptLogin}},
}
```


# Projects in Charles_pikachu

- [Games](https://github.com/CharlesPikachu/Games): Create interesting games by pure python.
- [DecryptLogin](https://github.com/CharlesPikachu/DecryptLogin): APIs for loginning some websites by using requests.
- [Musicdl](https://github.com/CharlesPikachu/musicdl): A lightweight music downloader written by pure python.
- [Videodl](https://github.com/CharlesPikachu/videodl): A lightweight video downloader written by pure python.
- [Pytools](https://github.com/CharlesPikachu/pytools): Some useful tools written by pure python.
- [PikachuWeChat](https://github.com/CharlesPikachu/pikachuwechat): Play WeChat with itchat-uos.
- [Pydrawing](https://github.com/CharlesPikachu/pydrawing): Beautify your image or video.
- [ImageCompressor](https://github.com/CharlesPikachu/imagecompressor): Image compressors written by pure python.
- [FreeProxy](https://github.com/CharlesPikachu/freeproxy): Collecting free proxies from internet.
- [Paperdl](https://github.com/CharlesPikachu/paperdl): Search and download paper from specific websites.
- [Sciogovterminal](https://github.com/CharlesPikachu/sciogovterminal): Browse "The State Council Information Office of the People's Republic of China" in the terminal.
- [CodeFree](https://github.com/CharlesPikachu/codefree): Make no code a reality.
- [DeepLearningToys](https://github.com/CharlesPikachu/deeplearningtoys): Some deep learning toys implemented in pytorch.
- [DataAnalysis](https://github.com/CharlesPikachu/dataanalysis): Some data analysis projects in charles_pikachu.
- [Imagedl](https://github.com/CharlesPikachu/imagedl): Search and download images from specific websites.
- [Pytoydl](https://github.com/CharlesPikachu/pytoydl): A toy deep learning framework built upon numpy.
- [NovelDL](https://github.com/CharlesPikachu/noveldl): Search and download novels from some specific websites.


# More

### WeChat Official Accounts

*Charles_pikachu*  
![img](./docs/pikachu.jpg)