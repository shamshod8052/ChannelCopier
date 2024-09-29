from typing import Optional

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Admin.models import User, Channel
from aio_bot.buttons import my_channel_kb, cancel
from aio_bot.config import DEFAULT_LANG
from aio_bot.filters.filters import IsAdminFilter
from aio_bot.loader import dp
from aio_bot.states import MyChannelForm
from enums import Texts


@dp.message(IsAdminFilter(), F.text.in_(Texts.MY_CHANNEL.values()))
async def my_channel(message: Message, state: FSMContext):
    await state.set_state(MyChannelForm.MyChannel)
    await message.answer(Texts.INPUT_MY_CHANNEL[DEFAULT_LANG], reply_markup=await my_channel_kb())


@dp.message(IsAdminFilter(), F.text.in_(Texts.CHANGE.values()), MyChannelForm.MyChannel)
async def add_channel(message: Message, state: FSMContext):
    await message.answer(Texts.SEND_CHANNEL[DEFAULT_LANG], reply_markup=await cancel())
    await state.set_state(MyChannelForm.GetMyChannel)


@dp.message(MyChannelForm.GetMyChannel)
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
        user.channel_for_send = channel
        user.save()
        await message.answer(Texts.ADDED_CHANNEL[DEFAULT_LANG], reply_markup=await my_channel_kb())
        await state.set_state(MyChannelForm.MyChannel)
    except:
        await message.answer(Texts.NOT_ADD_CHANNEL[DEFAULT_LANG])


@dp.message(IsAdminFilter(), F.text.in_(Texts.REMOVE.values()), MyChannelForm.MyChannel)
async def input_channel_for_remove(message: Message, state: FSMContext):
    await message.answer(Texts.INPUT_CHANNEL_FOR_REMOVE[DEFAULT_LANG],
                         reply_markup=await my_channel_kb(cancel_kb=True))
    await state.set_state(MyChannelForm.RemoveChannel)


@dp.message(MyChannelForm.RemoveChannel)
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
            user.channel_for_send = None
            user.save()
    except:
        await message.answer(Texts.NOT_REMOVE_CHANNEL[DEFAULT_LANG])
    else:
        user.refresh_from_db()
        await message.answer(Texts.REMOVED_CHANNEL[DEFAULT_LANG], reply_markup=await my_channel_kb(user))
        await state.set_state(MyChannelForm.MyChannel)


@dp.message(MyChannelForm.MyChannel, IsAdminFilter())
async def channel_info(message: Message):
    user = User.objects.get(chat_id=message.chat.id)
    if not user.channel_for_send:
        return
    channel: Optional[Channel] = user.channel_for_send
    text = (f"♻️ <b>Fullname:</b> <i>{channel.full_name if channel.full_name else '❌'}</i>"
            f"\n👤 <b>Username:</b> <i>{('@' + channel.username) if channel.username else '❌'}</i>"
            f"\n👤 <b>Telegram ID:</b> <i>{channel.chat_id}</i>")
    await message.reply(text)
