from aiogram.types import Message

from aio_bot.filters.filters import IsNotAdminFilter
from aio_bot.loader import dp


@dp.message(IsNotAdminFilter())
async def check(message: Message):
    return
