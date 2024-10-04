import asyncio
import datetime
import logging
import sys

from telethon import TelegramClient

from user_bot.loader import client


async def on_startup_notify(client_: TelegramClient) -> None:
    me = await client_.get_me()
    print(f"############ Bot ishga tushdi | ID: {me.id} | USERNAME: @{me.username} ############")
    print(f"Started time: {datetime.datetime.now()}")


async def main():
    from setup_django import set_django
    await set_django()
    from user_bot import handlers
    await client.connect()
    await on_startup_notify(client)
    await client.run_until_disconnected()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
