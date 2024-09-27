import asyncio
import datetime
import logging
import sys

from aiogram import Bot
from aiogram.types import BotCommand

from aio_bot.config import ADMINS
from aio_bot.loader import dp, bot

commands = {
    'commands': [
        BotCommand(command='start', description='Start the bot'),
    ],
}


async def set_commands(bot: Bot):
    await bot.set_my_commands(**commands)


async def on_startup_notify(bot: Bot):
    bot_ = await bot.me()
    print(f"############ Bot ishga tushdi | ID: {bot_.id} | USERNAME: @{bot_.username} ############")
    print(f"Started time: {datetime.datetime.now()}")

    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)


async def main() -> None:
    from setup_django import set_django
    await set_django()
    from aio_bot import handlers
    await set_commands(bot)
    await on_startup_notify(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    asyncio.run(main())
