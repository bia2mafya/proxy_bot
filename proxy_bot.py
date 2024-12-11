import os
from telethon import TelegramClient
import httpx

# دریافت API ID و API HASH از متغیرهای محیطی
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# کانال‌های منبع و مقصد
source_channels = ['ProxyMTProto', 'MTProxyStar']
output_channel = 'https://t.me/proxyhuuub'
custom_message = "\n\nکانال ما: @proxyhuuub"

# کلاینت تلگرام
client = TelegramClient('proxy_bot', api_id, api_hash)

async def fetch_proxies():
    """دریافت پروکسی از کانال‌های منبع"""
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
    """اجرای برنامه اصلی"""
    proxies = await fetch_proxies()
    valid_proxies = [proxy for proxy in proxies if await test_proxy(proxy)]
    await send_proxies(valid_proxies)

# اجرای برنامه
with client:
    client.loop.run_until_complete(main())
