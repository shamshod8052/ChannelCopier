import asyncio
import datetime
import logging
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import TelegramClient

from UserBot.config import PHONE_NUMBER, INTERVAL_SECONDS
from UserBot.loader import client


async def on_startup_notify(client_: TelegramClient) -> None:
    me = await client_.get_me()
    fullname = me.first_name or '' + (f' {me.last_name}' if me.last_name else '')
    logging.info(f"Run polling for user @{me.username} id={me.id} - '{fullname}'")
    logging.info(f"Running time {datetime.datetime.now()}")


async def scheduler():
    from UserBot.copy_process import copy_manager
    schedule = AsyncIOScheduler(timezone='Asia/Tashkent')
    schedule.add_job(copy_manager, trigger='interval', seconds=INTERVAL_SECONDS, id='copier')
    schedule.start()


async def main():
    from setup_django import set_django
    await set_django()
    await client.start(phone=PHONE_NUMBER)
    logging.info(f"Client started")
    await on_startup_notify(client)
    from UserBot import handlers
    await scheduler()
    await client.run_until_disconnected()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
