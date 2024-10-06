from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Admin.models import Channel
from aio_bot.config import DEFAULT_LANG
from enums import Texts


async def menu(user):
    kb = [
        [
            KeyboardButton(text=Texts.CHANNELS[DEFAULT_LANG]),
        ],
    ]
    if user.is_admin:
        kb.extend(
            [
                [
                    KeyboardButton(text=Texts.MY_CHANNEL[DEFAULT_LANG]),
                ]
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


async def channels_kb(cancel_kb=False, goal=Channel.Goals.get):
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
    channels = Channel.objects.filter(goal=goal)
    for n, channel in enumerate(channels.all()):
        name = f"@{channel.username}" if channel.username else channel.full_name if channel.full_name else channel.chat_id if channel.chat_id else 'x'
        name.replace('https://t.me/', '')
        kb.append(
            [
                KeyboardButton(text=f"{n + 1}. " + name)
            ]
        )

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
