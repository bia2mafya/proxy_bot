from telethon import TelegramClient, events
import requests

# اطلاعات API
API_ID = "21202654"
API_HASH = "cd42723946486d1f57c5840f351f3820"
BOT_TOKEN = "7371555081:AAHj72FOZ8WJFc3pTXicMuZGhAKviqX1IzY"

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

# هندلر پیام‌ها
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handle_new_message(event):
    proxy_url = event.message.text

    # تست پروکسی
    if proxy_url.startswith("https://t.me/proxy") and test_proxy(proxy_url):
        await bot_client.send_message(DESTINATION_CHANNEL, f"پروکسی فعال: {proxy_url}")
        print(f"پروکسی ارسال شد: {proxy_url}")
    else:
        print("پروکسی نامعتبر یا غیرفعال.")

# شروع برنامه
async def main():
    async with client:
        print("Listening for new messages...")
        await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
