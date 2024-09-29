from typing import Optional

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Admin.models import User, Channel
from aio_bot.buttons import menu, channels_kb, cancel
from aio_bot.config import DEFAULT_LANG
from aio_bot.filters.filters import IsHaveChannelFilter, get_channel, IsAdminFilter, IsHaveBossFilter
from aio_bot.loader import dp
from aio_bot.states import ChannelForm
from enums import Texts


@dp.message(F.text.in_(Texts.MAIN_MENU.values()))
@dp.message(IsAdminFilter(), F.text.in_(Texts.CANCEL.values()))
@dp.message(IsHaveBossFilter(), F.text.in_(Texts.CANCEL.values()))
@dp.message(IsAdminFilter(), Command('start'))
@dp.message(IsHaveBossFilter(), Command('start'))
async def start(message: Message, state: FSMContext):
    user, cr = User.objects.get_or_create(chat_id=message.chat.id)
    user.full_name = message.chat.full_name
    user.username = message.chat.username
    user.save()
    await state.set_state(None)
    await message.answer(Texts.HELLO[DEFAULT_LANG] + ' ' + message.from_user.full_name, reply_markup=await menu(user))


@dp.message(F.text.in_(Texts.MAIN_MENU.values()))
@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    user, cr = User.objects.get_or_create(chat_id=message.chat.id)
    user.full_name = message.chat.full_name
    user.username = message.chat.username
    user.save()
    await state.set_state(None)
    await message.answer(Texts.HELLO[DEFAULT_LANG] + ' ' + message.from_user.full_name)


@dp.message(IsAdminFilter(), F.text.in_(Texts.CHANNELS.values()))
@dp.message(IsHaveBossFilter(), F.text.in_(Texts.CHANNELS.values()))
async def my_channels(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    await message.answer(Texts.YOUR_CHANNELS[DEFAULT_LANG], reply_markup=await channels_kb(user))
    await state.set_state(ChannelForm.Channel)


@dp.message(IsAdminFilter(), F.text.in_(Texts.ADD.values()), ChannelForm.Channel)
@dp.message(IsHaveBossFilter(), F.text.in_(Texts.ADD.values()), ChannelForm.Channel)
async def add_channel(message: Message, state: FSMContext):
    await message.answer(Texts.SEND_CHANNEL[DEFAULT_LANG], reply_markup=await cancel())
    await state.set_state(ChannelForm.GetChannel)


@dp.message(ChannelForm.GetChannel)
async def get_channel_form(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    chat = message.forward_from_chat
    if not (chat and chat.type == 'channel'):
        await message.answer(Texts.NOT_FOUND_CHANNEL[DEFAULT_LANG])
        return
    channel, cr = Channel.objects.get_or_create(chat_id=chat.id)
    channel.full_name = chat.full_name
    channel.username = chat.username
    channel.save()
    try:
        user.channels.add(channel)
        user.refresh_from_db()
        await message.answer(Texts.ADDED_CHANNEL[DEFAULT_LANG], reply_markup=await channels_kb(user))
        await state.set_state(ChannelForm.Channel)
    except:
        await message.answer(Texts.NOT_ADD_CHANNEL[DEFAULT_LANG])


@dp.message(IsAdminFilter(), F.text.in_(Texts.REMOVE.values()), ChannelForm.Channel)
@dp.message(IsHaveBossFilter(), F.text.in_(Texts.REMOVE.values()), ChannelForm.Channel)
async def input_channel_for_remove(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    await message.answer(Texts.INPUT_CHANNEL_FOR_REMOVE[DEFAULT_LANG],
                         reply_markup=await channels_kb(user, cancel_kb=True))
    await state.set_state(ChannelForm.RemoveChannel)


@dp.message(ChannelForm.RemoveChannel)
async def get_channel_for_remove(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    info = message.text[message.text.find(' ') + 1:]
    info = info.replace('@', '')
    for t in ['full_name', 'username', 'chat_id']:
        kwargs = {t: info}
        try:
            channel = Channel.objects.get(**kwargs)
            break
        except:
            channel = None

    try:
        if channel:
            user.channels.remove(channel)
    except:
        await message.answer(Texts.NOT_REMOVE_CHANNEL[DEFAULT_LANG])
    else:
        user.refresh_from_db()
        await message.answer(Texts.REMOVED_CHANNEL[DEFAULT_LANG], reply_markup=await channels_kb(user))
        await state.set_state(ChannelForm.Channel)


@dp.message(ChannelForm.Channel, IsAdminFilter(), IsHaveChannelFilter())
@dp.message(ChannelForm.Channel, IsHaveBossFilter(), IsHaveChannelFilter())
async def channel_info(message: Message):
    user = User.objects.get(chat_id=message.chat.id)
    channel: Optional[Channel] = await get_channel(user.channels, message.text)
    text = (f"♻️ <b>Fullname:</b> <i>{channel.full_name if channel.full_name else '❌'}</i>"
            f"\n👤 <b>Username:</b> <i>{('@' + channel.username) if channel.username else '❌'}</i>"
            f"\n👤 <b>Telegram ID:</b> <i>{channel.chat_id}</i>")
    await message.reply(text)
