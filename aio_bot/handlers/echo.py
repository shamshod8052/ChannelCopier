from aiogram.types import Message

from aio_bot.config import DEFAULT_LANG
from aio_bot.loader import dp
from enums import Texts


@dp.message()
async def echo_(message: Message):
    await message.reply(Texts.SELECT_MENUS[DEFAULT_LANG])
