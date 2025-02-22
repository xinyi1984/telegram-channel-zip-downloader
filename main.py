import os
import time
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument

# 配置信息
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
session = 'session'
offset_id = 171  # 从偏移量171开始
message_limit = 5  # 每次查询5条消息
channel_username = 'juejijianghu'

# 创建Telegram客户端
client = TelegramClient(session, api_id, api_hash)

def bytes_to_mb(bytes):
    """将字节数转换为MB单位"""
    mb = bytes / (1024 * 1024)
    return "{:.2f} MB".format(mb)

async def upload_progress_callback(uploaded_bytes, total_bytes):
    """上传进度回调函数"""
    global start_time, previous_uploaded_bytes, previous_time
    current_time = time.time()
    current_uploaded_bytes = uploaded_bytes
    uploaded_since_last_time = current_uploaded_bytes - previous_uploaded_bytes
    time_since_last_time = current_time - previous_time

    if time_since_last_time > 0:
        speed = uploaded_since_last_time / time_since_last_time  # 网速，单位为字节/秒
    else:
        speed = 0

    print('\r\t\t\t\t -- Uploaded', bytes_to_mb(uploaded_bytes), '/', bytes_to_mb(total_bytes),
          ' (', "{:.2f}".format(speed / (1024 * 1024)), 'MB/s )', end='', flush=True)

    previous_uploaded_bytes = current_uploaded_bytes
    previous_time = current_time

async def get_channel_message_count():
    """获取频道总消息数量"""
    channel_entity = await client.get_entity(channel_username)
    messages = await client.get_messages(channel_entity)
    total_messages = messages.total
    print("当前频道共有消息数量: ", total_messages)

async def download_media():
    """获取频道消息，并下载视频消息"""
    global offset_id
    channel_entity = await client.get_entity(channel_username)

    while True:
        # 每次查询message_limit条消息
        messages = await client.get_messages(channel_entity, limit=message_limit, offset_id=offset_id)

        print("\n查到消息数量: ", len(messages), '偏移id', offset_id)
        if not messages:
            break

        for message in messages:
            if message.media and isinstance(message.media, MessageMediaDocument):
                # 检查MIME类型是否为zip
                if 'zip' not in message.media.document.mime_type:
                    continue

                # 创建保存目录
                file_path = 'files/' + channel_username + "/"
                os.makedirs(file_path, exist_ok=True)

                # 如果是消息组，保存到同一个文件夹
                if message.grouped_id is not None:
                    file_name = f"{message.grouped_id}/{message.id}.zip"
                else:
                    file_name = message.media.document.attributes[0].file_name

                file_name = file_path + file_name
                print("\n开始下载: ", file_name)
                await client.download_media(message=message, file=file_name,
                                            progress_callback=upload_progress_callback)

        # 更新偏移量
        offset_id = messages[-1].id

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
