import asyncio
import datetime
import logging
import sys

from telethon import TelegramClient
from telethon.events import Album, NewMessage, MessageEdited, MessageDeleted

from user_bot.config import NUMBER
from user_bot.loader import client


async def on_startup_notify(client_: TelegramClient) -> None:
    me = await client_.get_me()
    print(f"############ Bot ishga tushdi | ID: {me.id} | USERNAME: @{me.username} ############")
    print(f"Started time: {datetime.datetime.now()}")


async def main():
    from setup_django import set_django
    await set_django()
    await client.start(phone=NUMBER)
    await on_startup_notify(client)
    from user_bot.handlers import handle_media_group, handle_deleted_message, handle_new_message, handle_edited_message
    client.add_event_handler(handle_media_group, Album)
    client.add_event_handler(handle_new_message, NewMessage)
    client.add_event_handler(handle_edited_message, MessageEdited)
    client.add_event_handler(handle_deleted_message, MessageDeleted)
    await client.run_until_disconnected()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
