import os
import time
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument, DocumentAttributeFilename

# ************************************************************
#                       配置信息
# ************************************************************
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
session = 'session'
channel_username = 'juejijianghu'
download_limit = 5
# ************************************************************

client = TelegramClient(session, api_id, api_hash)

def bytes_to_mb(bytes):
    """字节转MB显示"""
    return f"{bytes/(1024*1024):.2f} MB"

async def upload_progress_callback(uploaded, total):
    """实时下载进度显示"""
    global start_time, prev_uploaded
    elapsed = time.time() - start_time
    speed = (uploaded - prev_uploaded) / max(elapsed, 0.1)
    print(f"\r\t下载进度 {bytes_to_mb(uploaded)}/{bytes_to_mb(total)}"
          f" | 速度 {speed/1024:.2f} MB/s", end='', flush=True)
    prev_uploaded = uploaded

async def fetch_latest_zip():
    """严格保持独立文件路径结构"""
    channel = await client.get_entity(channel_username)
    messages = await client.get_messages(channel, limit=download_limit)
    
    print(f"\n🔍 正在扫描频道最新 {len(messages)} 条消息...")
    for msg in messages:
        # 跳过非文档消息
        if not (msg.media and isinstance(msg.media, MessageMediaDocument)):
            continue
            
        doc = msg.media.document
        # 双重验证：mime_type和文件名后缀
        if 'zip' not in doc.mime_type.lower():
            continue

        # 强制获取原始文件名
        filename_attr = next((attr for attr in doc.attributes 
                            if isinstance(attr, DocumentAttributeFilename)), None)
        if not filename_attr:
            print(f"\n⚠️ 消息 {msg.id} 缺少文件名属性，已跳过")
            continue
        
        # 检查文件名是否以“真心”开头
        file_name = filename_attr.file_name
        if not file_name.startswith("真心"):
            continue    

        # 构建存储路径
        base_dir = os.path.join('files', channel_username)
        file_name = filename_attr.file_name
        save_path = os.path.join(base_dir, file_name)
        
        # 存在性检查
        if os.path.exists(save_path):
            print(f"\n⏭️ 文件已存在: {save_path}")
            continue
            
        # 创建目录并下载
        os.makedirs(base_dir, exist_ok=True)
        print(f"\n🚀 发现新文件: {file_name} (大小: {bytes_to_mb(doc.size)})")
        
        global start_time, prev_uploaded
        start_time = time.time()
        prev_uploaded = 0
        try:
            await client.download_media(msg, file=save_path, 
                                      progress_callback=upload_progress_callback)
            print(f"\n\n✅ 下载完成: {save_path}")
            return True
        except Exception as e:
            print(f"\n❌ 下载失败: {str(e)}")
            return False
        
    print("\n❌ 未在最新消息中发现新ZIP文件")
    return False

if __name__ == "__main__":
    with client:
        print("启动Telegram文件下载器...")
        client.loop.run_until_complete(fetch_latest_zip())
    print("程序执行完毕")
