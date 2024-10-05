from telethon import TelegramClient

from user_bot.config import NUMBER, API_ID, API_HASH

client = TelegramClient(f"user_bot/sessions/{NUMBER}", API_ID, API_HASH, sequential_updates=True)
