import os
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# خواندن توکن ربات از متغیرهای محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ایجاد ربات
bot = Bot(token=BOT_TOKEN)

# شناسه کانال مقصد
DESTINATION_CHANNEL = "@proxyhuuub"

# تابع برای ارسال پیام
def send_proxy(update, context):
    message_text = update.message.text
    if message_text.startswith("https://t.me/proxy"):
        # ارسال پروکسی به کانال مقصد
        context.bot.send_message(chat_id=DESTINATION_CHANNEL, text=f"پروکسی فعال: {message_text}")
        print(f"پروکسی ارسال شد: {message_text}")
    else:
        print("پیام غیر معتبر دریافت شد.")

# تنظیمات و شروع دریافت پیام‌ها
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # هندلر برای پیام‌های جدید
    message_handler = MessageHandler(Filters.text & ~Filters.command, send_proxy)
    dispatcher.add_handler(message_handler)

    # شروع دریافت پیام‌ها
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
