import logging

from telethon import TelegramClient

from user_bot.config import NUMBER, API_ID, API_HASH

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)  # Name the logger after the current module

client = TelegramClient(f"user_bot/sessions/{NUMBER}", API_ID, API_HASH)
