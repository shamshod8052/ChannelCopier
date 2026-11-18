from telethon import TelegramClient

from UserBot.config import PHONE_NUMBER, API_ID, API_HASH, PROXY

# PROXY=socks5://127.0.0.1:1080 in .env; empty means a direct connection
proxy = None
if PROXY:
    scheme, address = PROXY.split('://', 1)
    host, port = address.rsplit(':', 1)
    proxy = (scheme, host, int(port))

client = TelegramClient(
     f"UserBot/sessions/{PHONE_NUMBER}", API_ID, API_HASH, proxy=proxy
)
