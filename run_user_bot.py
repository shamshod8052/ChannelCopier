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
    await on_startup_notify(client)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    client.start()
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
