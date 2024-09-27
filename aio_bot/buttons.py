from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aio_bot.config import DEFAULT_LANG
from enums import Texts


async def menu():
    kb = [
        [
            KeyboardButton(text=Texts.CHANNELS[DEFAULT_LANG]),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


async def cancel():
    kb = [
        [
            KeyboardButton(text=Texts.CANCEL[DEFAULT_LANG]),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


async def channels_kb(user, cancel_kb=False):
    if cancel_kb:
        kb = [
            [
                KeyboardButton(text=Texts.CANCEL[DEFAULT_LANG]),
            ]
        ]
    else:
        kb = [
            [
                KeyboardButton(text=Texts.ADD[DEFAULT_LANG]),
                KeyboardButton(text=Texts.REMOVE[DEFAULT_LANG]),
            ]
        ]

    for n, channel in enumerate(user.channels.all()):
        name = channel.full_name or channel.username or channel.chat_id
        name.replace('https://t.me/', '@')
        kb.append(
            [
                KeyboardButton(text=f"{n + 1}. " + name)
            ]
        )

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
