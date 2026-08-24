from telethon import TelegramClient

from UserBot.config import PHONE_NUMBER, API_ID, API_HASH

proxy = ('socks5', '127.0.0.1', 1080)

client = TelegramClient(
     f"UserBot/sessions/{PHONE_NUMBER}", API_ID, API_HASH, proxy=proxy
)
