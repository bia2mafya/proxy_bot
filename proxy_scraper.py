import os
from telethon import TelegramClient, events
import requests

# خواندن مقادیر از متغیرهای محیطی
API_ID = int(os.getenv("API_ID"))  # API_ID باید عدد صحیح باشد
API_HASH = os.getenv("API_HASH")  # API_HASH باید یک رشته باشد
BOT_TOKEN = os.getenv("BOT_TOKEN")  # BOT_TOKEN برای ارسال پیام به کانال مقصد

# کانال‌ها
SOURCE_CHANNEL = "ProxyMTProto"  # کانال منبع (بدون @)
DESTINATION_CHANNEL = "@proxyhuuub"  # کانال مقصد

# اتصال به کلاینت
client = TelegramClient("proxy_session", API_ID, API_HASH)
bot_client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# تابع تست پروکسی
def test_proxy(proxy_url):
    try:
        # استخراج اطلاعات پروکسی از URL
        params = proxy_url.split("?")[1]
        data = dict(param.split("=") for param in params.split("&"))

        server = data.get("server")
        port = int(data.get("port"))
        secret = data.get("secret")

        # پیکربندی پروکسی MTProto
        proxies = {
            "http": f"socks5://{server}:{port}",
            "https": f"socks5://{server}:{port}"
        }

        # ارسال یک درخواست تستی
        response = requests.get("https://api.telegram.org", proxies=proxies, timeout=5)

        return response.status_code == 200  # بازگشت True اگر پروکسی فعال است
    except Exception as e:
        print(f"خطا در تست پروکسی: {e}")
        return False

