import os
import time
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument

# ************************************************************
#                       配置信息
# ************************************************************
# 申请并替换为你的 api_id 和 api_hash
#
# 在 my.telegram.org 页面 输入手机号和网页验证码 登录管理后台
# 点击 API development tools 进入 Create new application 页面
# 填写资料点击创建 会生成 api_id api_hash
# 网页点击 create application 按钮创建时 经常会提示失败
# 没有明确的解决方法 在不同的时段多试几次 有几率就成功了 有时候好几天都不行
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')

# 定义会话名称，可以随便指定，确保唯一即可
#
# 第一次登录时在控制台需要输入一次手机号
# 然后 telegram 会给你的网页版发一条验证码消息
# 将验证码输入到控制台 创建 session 文件
# 有了 session 文件以后 不要删除 下一次就可以直接启动不需要进行验证了
session ='session'

# 消息偏移点 id，表示从哪一条消息开始下载，可以忽略之前已经处理过的消息
offset_id = 165

# 每次查询的消息数量
message_limit = 5

# 想要下载的频道用户名，如果频道地址是 https://t.me/abc，那么频道名称为 "abc"
channel_username = 'juejijianghu'

# ************************************************************
#                       配置结束
# ************************************************************

# 创建一个 client
client = TelegramClient(session, api_id, api_hash)


def bytes_to_mb(bytes):
    """
    将字节数转换为以 MB 为单位的字符串格式
    """
    mb = bytes / (1024 * 1024)
    return "{:.2f} MB".format(mb)  # 格式化输出字节数转换后的结果，保留两位小数


# 显示下载进度 可以不配置
async def upload_progress_callback(uploaded_bytes, total_bytes):
    """
    上传进度回调函数
    """
    global start_time, previous_uploaded_bytes, previous_time
    current_time = time.time()  # 获取当前时间
    current_uploaded_bytes = uploaded_bytes  # 获取当前已上传的字节数
    uploaded_since_last_time = current_uploaded_bytes - previous_uploaded_bytes  # 计算本次上传的字节数
    time_since_last_time = current_time - previous_time  # 计算时间间隔

    if time_since_last_time > 0:
        speed = uploaded_since_last_time / time_since_last_time  # 计算网速（字节/秒）
    else:
        speed = 0

    print('\r\t\t\t\t -- Uploaded', bytes_to_mb(uploaded_bytes), '/', bytes_to_mb(total_bytes),
          ' (', "{:.2f}".format(speed / (1024 * 1024)), 'MB/s )', end='', flush=True)  # 打印上传进度

    previous_uploaded_bytes = current_uploaded_bytes  # 更新上次上传的字节数
    previous_time = current_time  # 更新上次时间


async def get_channel_message_count():
    """
    获取频道总消息数量
    """
    global channel_username
    channel_entity = await client.get_entity(channel_username)  # 获取频道实体
    messages = await client.get_messages(channel_entity)  # 获取频道消息
    total_messages = messages.total
    print("当前频道共有消息数量: ", total_messages)  # 打印消息数量


async def download_media():
    """
    获取频道消息，并下载最新的 5 条消息中有其它类型文件的消息中最新的一条 ZIP 文件
    """
    global channel_username
    channel_entity = await client.get_entity(channel_username)  # 获取频道实体

    offset = offset_id
    while True:

        # 每次查询 5 条消息
        messages = await client.get_messages(channel_entity, limit=message_limit, reverse=True, offset_id=offset)

        print("\n查到消息数量: ", len(messages), '偏移 id', offset)  # 打印查询到的消息数量和偏移量
        if not messages:
            break

        latest_zip_message = None  # 用于存储最新的 ZIP 消息

        for message in messages:
            # 检查是否有媒体文件且为文档类型
            if message.media and isinstance(message.media, MessageMediaDocument):
                # 检查文件类型是否为 ZIP
                if'mime_type' in message.media.document.attributes[0] and'mime_type' in message.media.document.attributes[0] and 'zip' in message.media.document.attributes[0]['mime_type']:
                    latest_zip_message = message  # 存储为最新的 ZIP 消息
                else:
                    continue  # 不是 ZIP 类型，继续下一个消息

        if latest_zip_message:  # 如果找到了最新的 ZIP 消息
            # 只保留 zip
            print("\nmime_type: ", latest_zip_message.media.document.attributes[0].file_name)
            if latest_zip_message.media.document.mime_type!= 'application/zip':
                continue

            file_path = 'files/' + channel_username + "/"

            # 如果是消息组 那么保存到同一个文件夹里
            if latest_zip_message.grouped_id is not None:
                file_name = f"{latest_zip_message.grouped_id}/{latest_zip_message.id}.zip"
            else:
                file_name = f"{latest_zip_message.media.document.attributes[0].file_name}"

            file_name = file_path + file_name
            print("\n开始下载: ", file_name)
            await client.download_media(message=latest_zip_message, file=file_name,
                                        progress_callback=upload_progress_callback)
            break

        # 更新偏移量
        offset = offset + message_limit


print('starting....')

with client:
    start_time = time.time()
    previous_uploaded_bytes = 0
    previous_time = start_time

    # 获取频道消息数量
    client.loop.run_until_complete(get_channel_message_count())

    # 获取并下载频道消息
    client.loop.run_until_complete(download_media())

print('\ndone....')
