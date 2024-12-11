from telethon import TelegramClient, events
import httpx
import os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')

source_channels = ['ProxyMTProto', 'MTProxyStar']
output_channel = 'https://t.me/proxyhuuub'

custom_message = "\n\nکانال ما: @proxyhuuub"

client = TelegramClient('proxy_bot', api_id, api_hash)

async def fetch_proxies():
    proxies = []
    for channel in source_channels:
        async for message in client.iter_messages(channel, limit=50):
            if message.text and (":" in message.text):
                proxies.append(message.text + custom_message)
    return proxies

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

async def send_proxies(proxies):
    for proxy in proxies:
        await client.send_message(output_channel, proxy)

async def main():
    await client.start(bot_token=bot_token)  # استفاده از توکن بات
    proxies = await fetch_proxies()
    valid_proxies = []
    for proxy in proxies:
        if await test_proxy(proxy):
            valid_proxies.append(proxy)
    await send_proxies(valid_proxies)

with client:
    client.loop.run_until_complete(main())
