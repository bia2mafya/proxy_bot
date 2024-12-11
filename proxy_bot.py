import os
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import httpx

# اطلاعات مربوط به توکن بات
bot_token = os.getenv('BOT_TOKEN')  # توکن بات از متغیر محیطی دریافت می‌شود

# کانال‌ها برای دریافت پروکسی و ارسال آن‌ها
source_channels = ['ProxyMTProto', 'MTProxyStar']
output_channel = '@proxyhuuub'

# پیام اضافی به پروکسی‌ها
custom_message = "\n\nکانال ما: @proxyhuuub"

# ایجاد یک Bot با استفاده از توکن
bot = Bot(token=bot_token)

# این تابع پیام‌ها را از کانال‌های مشخص شده دریافت می‌کند
async def fetch_proxies():
    proxies = []
    for channel in source_channels:
        # استفاده از API تلگرام برای دریافت پیام‌ها از کانال‌ها
        messages = bot.get_chat_history(channel, limit=50)
        for message in messages:
            if message.text and (":" in message.text):
                proxies.append(message.text + custom_message)
    return proxies

# این تابع پروکسی‌ها را تست می‌کند
async def test_proxy(proxy):
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

# این تابع پروکسی‌های معتبر را به کانال ارسال می‌کند
async def send_proxies(proxies):
    for proxy in proxies:
        await bot.send_message(output_channel, proxy)

# این تابع اصلی است که تمامی پروسه را مدیریت می‌کند
async def main():
    # دریافت پروکسی‌ها
    proxies = await fetch_proxies()

    # فیلتر کردن پروکسی‌های معتبر
    valid_proxies = []
    for proxy in proxies:
        if await test_proxy(proxy):
            valid_proxies.append(proxy)

    # ارسال پروکسی‌ها به کانال مقصد
    await send_proxies(valid_proxies)

if __name__ == "__main__":
    # اجرا کردن برنامه
    main()
