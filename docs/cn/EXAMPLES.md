# 实战案例


## 项目声明

本系列文章源代码仅供python学习交流，请勿用于商业等违法相关法律法规的用途，如有发现，我会直接删除这个系列的文章和代码。


## 安装方式

在终端运行如下命令即可(请保证python在环境变量中):

```sh
pip install DecryptLoginExamples --upgrade
```

另外部分程序依赖于ffmpeg和aria2c, 请确保这个两个工具在你的系统环境变量中可以被调用:

- [ffmpeg](https://ffmpeg.org/)
- [aria2c](https://aria2.github.io/)


## 项目汇总

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


## 使用简介

#### 微博监控

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
    'time_interval': 查询微博动态的间隔时间,
}
crawler_executor = client.Client()
crawler_executor.executor('weibomonitor', config=config)
```

#### 生成QQ个人专属报告

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
    'savedir': 生成的报告保存的文件夹,
}
crawler_executor = client.Client()
crawler_executor.executor('qqreports', config=config)
```

#### 下载B站指定UP主的所有视频

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('bilibiliuservideos', config=config)
```

#### 网易云个人歌单下载器

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('neteasesonglistdownloader', config=config)
```

#### 网易云个人听歌排行榜

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('neteaselistenleaderboard', config=config)
```

#### 下载指定微博用户的所有微博数据

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
}
crawler_executor = client.Client()
crawler_executor.executor('userweibospider', config=config)
```

#### 网易云音乐自动签到

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('neteasesignin', config=config)
```

#### 微博表情包爬取

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
}
crawler_executor = client.Client()
crawler_executor.executor('weiboemoji', config=config)
```

#### 大吼一声发微博

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
}
crawler_executor = client.Client()
crawler_executor.executor('weibosender', config=config)
```

#### 淘宝商品数据小爬虫

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('tbgoods', config=config)
```

#### 京东商品数据小爬虫

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('jdgoods', config=config)
```

#### 批量删除微博

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
}
crawler_executor = client.Client()
crawler_executor.executor('delallweibos', config=config)
```

#### 批量删除QQ空间说说

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('clearqzone', config=config)
```

#### 在终端看网易云每日歌曲推荐

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('neteaseeveryday', config=config)
```

#### 网易云音乐刷歌曲播放量

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
}
crawler_executor = client.Client()
crawler_executor.executor('neteaseclickplaylist', config=config)
```

#### 天翼云盘自动签到+抽奖

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
}
crawler_executor = client.Client()
crawler_executor.executor('cloud189signin', config=config)
```

#### 中国大学MOOC下载器

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+
- ffmpeg: 使用前请确保ffmpeg在环境变量中, [下载地址](https://ffmpeg.org/)

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'url': 课程链接, 例如: https://www.icourse163.org/course/SJTU-1003381021, 
}
crawler_executor = client.Client()
crawler_executor.executor('moocdl', config=config)
```

#### 修改小米运动中的步数

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
    'steps': 想要刷到的目标步数,
}
crawler_executor = client.Client()
crawler_executor.executor('modifymihealthsteps', config=config)
```

#### 淘宝抢购脚本

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
    'trybuy_interval': 抢购商品时查询商品是否可以购买的时间间隔(单位秒),
    'server_key': Server酱的Key,
}
crawler_executor = client.Client()
crawler_executor.executor('taobaosnap', config=config)
```

#### 京东抢购脚本

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
    'trybuy_interval': 抢购商品时查询商品是否可以购买的时间间隔(单位秒),
    'server_key': Server酱的Key,
    'paywd': 支付密码, 部分商品需要支付密码才能提交订单, 输入密码不会导致你直接购买商品, 请放心使用,
}
crawler_executor = client.Client()
crawler_executor.executor('jingdongsnap', config=config)
```

#### B站UP主监控

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
    'up_ids': 监控的UP主ID, 例如: ['406756145'],
    'time_interval': 查询UP主的动态的间隔时间,
    'server_key': Server酱的Key,
}
crawler_executor = client.Client()
crawler_executor.executor('bilibiliupmonitor', config=config)
```

#### B站监控关注的UP主并自动转发抽奖

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用于存储历史cookies的唯一标识ID, 
    'time_interval': 查询UP主的动态的间隔时间,
}
crawler_executor = client.Client()
crawler_executor.executor('bilibililottery', config=config)
```

#### 微博水军

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
    'targetid': 想要流量造假服务的明星微博ID, 例如: '1776448504',
}
crawler_executor = client.Client()
crawler_executor.executor('weibowater', config=config)
```

#### 微博批量拉黑脚本

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
    'blacklist_ids': 想要批量拉黑的用户列表, 例如: ['1776448504', '1792951112', '2656274875'],
}
crawler_executor = client.Client()
crawler_executor.executor('weiboblacklist', config=config)
```

#### 微博自动转发抽奖

**1.相关依赖**

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：

```sh
pip install DecryptLoginExamples
```

**2.环境配置**

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

**3.调用方式**

脚本调用方式如下：

```python
from DecryptLoginExamples import client

config = {
    'username': 用户名,
    'password': 密码,
    'time_interval': 查询微博动态的间隔时间,
}
crawler_executor = client.Client()
crawler_executor.executor('weibolottery', config=config)
```