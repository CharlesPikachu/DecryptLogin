# 实战案例


## 项目汇总

|  项目名称                       |   微信公众号文章简介                                             |   源代码                                                                                                     |
|  :----:                         |   :----:                                                         |   :----:                                                                                                     |
|  微博监控                       |   [click](https://mp.weixin.qq.com/s/uOT1cGqXkOq-Hdc8TVnglg)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/weiboMonitor)                  |
|  生成QQ个人专属报告             |	  [click](https://mp.weixin.qq.com/s/dsVtEp_TFeyeSAAUn1zFEw)     |	 [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/QQReports)                     |
|  下载B站指定UP主的所有视频      |   [click](https://mp.weixin.qq.com/s/GaVW4_nbAaO0QvphI7QgnA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/bilibiliDownloadUserVideos)    |
|  网易云个人歌单下载器           |   [click](https://mp.weixin.qq.com/s/_82U7luG6jmV-xb8-Qkiew)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/NeteaseSongListDownloader)     |
|  网易云个人听歌排行榜           |   [click](https://mp.weixin.qq.com/s/Wlf1a82oACc9N7zGezcy8Q)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/NeteaseListenLeaderboard)      |
|  下载指定微博用户的所有微博数据 |   [click](https://mp.weixin.qq.com/s/-3BDTZAE1x7nfCLNq2mFBw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/userWeiboSpider)               |
|  网易云音乐自动签到             |   [click](https://mp.weixin.qq.com/s/8d7smUSzW2ds1ypZq-yeFw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/NeteaseSignin)                 |
|  微博表情包爬取                 |   [click](https://mp.weixin.qq.com/s/QiPm4gyE8i5amR5gB3IbBA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/weiboEmoji)                    |
|  大吼一声发微博                 |   [click](https://mp.weixin.qq.com/s/_aIY-iVj3xetfHQyMxflkg)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/weiboSender)                   |
|  淘宝商品数据小爬虫             |   [click](https://mp.weixin.qq.com/s/NhK9eeWNXv_wPnolccRR-g)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/tbgoods)                       |
|  京东商品数据小爬虫             |   [click](https://mp.weixin.qq.com/s/LXheJveR248ZW4SP5F6fjw)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/jdgoods)                       |
|  批量删除微博                   |   [click](https://mp.weixin.qq.com/s/E5Erg10FvyutEKaB_JGufA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/delallweibos)                  |
|  批量删除QQ空间说说             |   [click](https://mp.weixin.qq.com/s/Fj9MQXXRZ8wuKiX3Tytx8A)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/ClearQzone)                    |
|  在终端看网易云每日歌曲推荐     |   [click](https://mp.weixin.qq.com/s/tliFa5CYVEirMEyUj0jPbg)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/NeteaseEveryday)               |
|  网易云音乐刷歌曲播放量         |   [click](https://mp.weixin.qq.com/s/BpoO55I-jxAGO_Vv32khlA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/NeteaseClickPlaylist)          |
|  天翼云盘自动签到+抽奖          |   [click](https://mp.weixin.qq.com/s/tSLTSKDMzMAkP2deCjkanA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/cloud189signin)                |
|  中国大学MOOC下载器             |   [click](https://mp.weixin.qq.com/s/KsXU-pMvT8GzpPWVpcWIOA)     |   [click](https://github.com/CharlesPikachu/DecryptLogin/tree/master/examples/moocdl)                        |


## 使用简介

#### 微博监控

1.相关依赖

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：
```sh
pip install DecryptLogin
```

2.环境配置

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

3.运行方式

脚本运行方式如下：

```sh
usage: weiboMonitor.py [-h] [-u USERNAME] [-p PASSWORD] [-i ID]
                       [-t TIME_INTERVAL]

微博监控

optional arguments:
  -h, --help        show this help message and exit
  -u USERNAME       用户名
  -p PASSWORD       密码
  -i ID             待监控用户id
  -t TIME_INTERVAL  监控的时间间隔
```

例如：
```sh
python weiboMonitor.py -u 用户名 -p 密码
```

#### 生成QQ个人专属报告

1.相关依赖

在终端运行如下命令即可安装运行该项目所需要的相关依赖包：
```sh
pip install DecryptLogin, wordcloud, pillow
```

2.环境配置

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+

3.运行方式

脚本运行方式如下：

```sh
python generate.py
```