# telegram-channel-zip-downloader

![Build](https://shields.io/github/actions/workflow/status/xinyi1984/telegram-channel-zip-downloader/Unzip pg and add pg.yml?branch=main&logo=github&label=Build)

## Credits
This repo relies on the following third-party projects:
- [xinyi1984/xytv](https://github.com/xinyi1984/xytv) (Updated: a545c27b99b6d6d9e54196b8a0adcf3b56a97ddf)


# 概述：
* 从 telegram 任意频道中下载该频道的全部历史视频。
* 支持偏移查询，可以从某条消息开始执行。

# 联系方式
* 问题修改 | 功能定制 | 沟通交流
* 请联系 telegram https://t.me/mexcmoe

# 使用条件
* python 3.9
* 需要在 my.telegram.org 页面申请自己的 api_id 和 api_hash

# 安装方法
```
$ git clone https://github.com/mexcmoe/telegram-channel-video-downloader.git
$ cd telegram-channel-video-downloader
$ pip install -r requirements.txt
```

# 配置和使用
```
$ 在main.py中配置一下从my.telegram.org创建好的api_id 和 api_hash
$ 配置channel_username = 你想下载的频道名称
$ 如果你曾经下载过，那么不想下载重复的部分，那么可以通过修改偏移量offset_id来跳过之前的消息
$ 视频文件名就是频道的消息id，将offset_id配置成上次执行完的最后一条id即可跳过之前的部分
$ 执行启动命令
$ python main.py
```



