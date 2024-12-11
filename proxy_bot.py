from telethon import TelegramClient, events
import httpx
import os

# اطلاعات مربوط به API تلگرام
api_id = os.getenv('API_ID')  # از متغیر محیطی دریافت می‌شود
api_hash = os.getenv('API_HASH')  # از متغیر محیطی دریافت می‌شود
bot_token = os.getenv('BOT_TOKEN')  # از متغیر محیطی دریافت می‌شود

# کانال‌ها برای دریافت پروکسی و ارسال آن‌ها
source_channels = ['ProxyMTProto', 'MTProxyStar']
output_channel = 'https://t.me/proxyhuuub'

# پیام اضافی به پروکسی‌ها
custom_message = "\n\nکانال ما: @proxyhuuub"

# ایجاد کلاینت تلگرام
client = TelegramClient('proxy_bot', api_id, api_hash)

async def fetch_proxies():
    """دریافت پیام‌ها از کانال‌های منبع"""
    proxies = []
    for channel in source_channels:
        async for message in client.iter_messages(channel, limit=50):
            if message.text and (":" in message.text):
                proxies.append(message.text + custom_message)
    return proxies

async def test_proxy(proxy):
    """تست پروکسی"""
    try:
        proxy_parts = proxy.split(':')
        host, port = proxy_parts[0], int(proxy_parts[1])
        proxies = {
            "http://": f"http://{host}:{port}",
            "https://": f"http://{host}:{port}"
        }
        async with httpx.AsyncClient(proxies=proxies, timeout=5) as client:
            response = await client.get('https://api.telegram.org')
            if response.status_code == 200:
                return True
    except Exception:
        return False
    return False

async def send_proxies(proxies):
    """ارسال پروکسی‌های معتبر به کانال مقصد"""
    for proxy in proxies:
        await client.send_message(output_channel, proxy)

async def main():
    # اتصال به بات
    await client.start(bot_token=bot_token)

    # دریافت پروکسی‌ها
    proxies = await fetch_proxies()

    # فیلتر کردن پروکسی‌های معتبر
    valid_proxies = []
    for proxy in proxies:
        if await test_proxy(proxy):
            valid_proxies.append(proxy)

    # ارسال پروکسی‌ها به کانال مقصد
    await send_proxies(valid_proxies)

# اجرای اسکریپت
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
