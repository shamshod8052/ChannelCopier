from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aio_bot.config import DEFAULT_LANG
from enums import Texts


async def menu(user):
    kb = [
        [
            KeyboardButton(text=Texts.CHANNELS[DEFAULT_LANG]),
        ],
    ]
    if user.is_admin:
        kb.append(
            [
                KeyboardButton(text=Texts.ADMINS[DEFAULT_LANG]),
            ]
        )

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
            ],
            [
                KeyboardButton(text=Texts.MAIN_MENU[DEFAULT_LANG]),
            ]
        ]

    for n, channel in enumerate(user.channels.all()):
        name = f"@{channel.username}" if channel.username else channel.full_name if channel.full_name else channel.chat_id if channel.chat_id else 'x'
        name.replace('https://t.me/', '')
        kb.append(
            [
                KeyboardButton(text=f"{n + 1}. " + name)
            ]
        )

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


async def admins_kb(user, cancel_kb=False):
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
            ],
            [
                KeyboardButton(text=Texts.MAIN_MENU[DEFAULT_LANG]),
            ]
        ]

    for n, admin in enumerate(user.admins.all()):
        name = f"@{admin.username}" if admin.username else admin.full_name if admin.full_name else admin.chat_id if admin.chat_id else 'x'
        name.replace('https://t.me/', '')
        kb.append(
            [
                KeyboardButton(text=f"{n + 1}. " + name)
            ]
        )

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
