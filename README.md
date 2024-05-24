# 概述：
* 从 telegram 任意频道中下载该频道的全部历史视频。
* 支持偏移查询，可以从某条消息开始执行。

# 联系方式
* 问题修改 | 功能定制 | 沟通交流
* 请联系 telegram https://t.me/klysys

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

**Getting chat id:**

**1. Using web telegram:**

1. Open <https://web.telegram.org/?legacy=1#/im>

2. Now go to the chat/channel and you will see the URL as something like
   - `https://web.telegram.org/?legacy=1#/im?p=u853521067_2449618633394` here `853521067` is the chat id.
   - `https://web.telegram.org/?legacy=1#/im?p=@somename` here `somename` is the chat id.
   - `https://web.telegram.org/?legacy=1#/im?p=s1301254321_6925449697188775560` here take `1301254321` and add `-100` to the start of the id => `-1001301254321`.
   - `https://web.telegram.org/?legacy=1#/im?p=c1301254321_6925449697188775560` here take `1301254321` and add `-100` to the start of the id => `-1001301254321`.

**2. Using bot:**

1. Use [@username_to_id_bot](https://t.me/username_to_id_bot) to get the chat_id of
    - almost any telegram user: send username to the bot or just forward their message to the bot
    - any chat: send chat username or copy and send its joinchat link to the bot
    - public or private channel: same as chats, just copy and send to the bot
    - id of any telegram bot
