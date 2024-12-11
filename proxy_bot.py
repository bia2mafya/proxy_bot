import os
from telegram import Bot
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

async def send_proxies(proxies):
    """ارسال پروکسی‌ها به کانال مقصد"""
    for proxy in proxies:
        try:
            # ارسال پروکسی به کانال
            await bot.send_message(output_channel, proxy)
        except Exception as e:
            print(f"Error sending message: {e}")

async def main():
    # فرض کنید پروکسی‌ها را از جایی دریافت کرده‌ایم
    proxies = ["123.45.67.89:8080", "98.76.54.32:9090"]

    # ارسال پروکسی‌ها به کانال مقصد
    await send_proxies(proxies)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
