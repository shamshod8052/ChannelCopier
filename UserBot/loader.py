from telethon import TelegramClient

from UserBot.config import PHONE_NUMBER, API_ID, API_HASH

client = TelegramClient(f"UserBot/sessions/{PHONE_NUMBER}", API_ID, API_HASH)
