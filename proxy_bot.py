import os
from telegram import Bot
import httpx

# اطلاعات مربوط به توکن بات
bot_token = os.getenv('BOT_TOKEN')  # توکن بات از متغیر محیطی دریافت می‌شود

# کانال فقط @ProxyMTProto برای دریافت پروکسی‌ها
source_channel = 'ProxyMTProto'

# کانال مقصد برای ارسال پروکسی‌ها
output_channel = '@proxyhuuub'

# پیام اضافی به پروکسی‌ها
custom_message = "\n\nکانال ما: @proxyhuuub"

# ایجاد یک Bot با استفاده از توکن
bot = Bot(token=bot_token)

# دریافت پیام‌ها از کانال @ProxyMTProto
async def fetch_proxies():
    proxies = []
    # دریافت پیام‌ها از کانال @ProxyMTProto
    messages = bot.get_chat_history(source_channel, limit=50)
    for message in messages:
        if message.text and (":" in message.text):
            proxies.append(message.text + custom_message)
    return proxies

# ارسال پروکسی‌ها به کانال مقصد
async def send_proxies(proxies):
    for proxy in proxies:
        try:
            # ارسال پروکسی به کانال
            await bot.send_message(output_channel, proxy)
        except Exception as e:
            print(f"Error sending message: {e}")

async def main():
    # دریافت پروکسی‌ها از کانال
    proxies = await fetch_proxies()

    # ارسال پروکسی‌ها به کانال مقصد
    await send_proxies(proxies)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
