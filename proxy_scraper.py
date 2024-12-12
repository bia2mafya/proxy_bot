import logging
import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# تنظیمات ورود برای لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن ربات تلگرام خود را اینجا قرار دهید
TOKEN = '7371555081:AAHj72FOZ8WJFc3pTXicMuZGhAKviqX1IzY'

# آدرس کانال‌ها
CHANNEL_IN = '@ProxyMTProto'
CHANNEL_OUT = '@proxyhuuub'

def start(update, context):
    """دستورات شروع برای ربات"""
    update.message.reply_text('ربات شروع به کار کرد.')

def check_proxy(proxy):
    """تست صحت پروکسی"""
    url = f"https://t.me/proxy?server={proxy['server']}&port={proxy['port']}&secret={proxy['secret']}"
    try:
        # ارسال درخواست به پروکسی
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False

def process_message(update, context):
    """پردازش پیام‌ها برای دریافت پروکسی‌ها"""
    # فرض می‌کنیم پیام‌های کانال به این شکل باشند:
    message_text = update.message.text
    if "server=" in message_text and "port=" in message_text and "secret=" in message_text:
        # پارس کردن پروکسی از فرمت پیام
        proxy_data = {}
        try:
            server = message_text.split("server=")[1].split("&")[0]
            port = message_text.split("port=")[1].split("&")[0]
            secret = message_text.split("secret=")[1]
            proxy_data = {"server": server, "port": port, "secret": secret}
        except IndexError:
            return

        # بررسی صحت پروکسی
        if check_proxy(proxy_data):
            # ارسال پروکسی سالم به کانال مقصد
            bot = Bot(token=TOKEN)
            bot.send_message(chat_id=CHANNEL_OUT, text=message_text)

def main():
    """برنامه اصلی ربات"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # دستورات ربات
    dp.add_handler(CommandHandler("start", start))

    # پردازش پیام‌ها از کانال ورودی
    dp.add_handler(MessageHandler(Filters.text & Filters.chat(CHANNEL_IN), process_message))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
