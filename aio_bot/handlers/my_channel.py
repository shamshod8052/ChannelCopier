import traceback

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Admin.models import User, Channel
from aio_bot.buttons import channels_kb, cancel
from aio_bot.config import DEFAULT_LANG
from aio_bot.filters.filters import get_channel
from aio_bot.loader import dp
from aio_bot.states import MyChannelForm
from enums import Texts


@dp.message(F.text.in_(Texts.MY_CHANNEL.values()))
async def my_channel(message: Message, state: FSMContext):
    await state.set_state(MyChannelForm.MyChannel)
    await message.answer(Texts.INPUT_MY_CHANNEL[DEFAULT_LANG], reply_markup=await channels_kb(goal=Channel.Goals.send))


@dp.message(F.text.in_(Texts.ADD.values()), MyChannelForm.MyChannel)
async def add_my_channel(message: Message, state: FSMContext):
    await message.answer(Texts.SEND_CHANNEL[DEFAULT_LANG], reply_markup=await cancel())
    await state.set_state(MyChannelForm.GetMyChannel)


@dp.message(MyChannelForm.GetMyChannel)
async def get_my_channel_func(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    chat = message.forward_from_chat
    if not (chat and chat.type == 'channel'):
        await message.answer(Texts.NOT_FOUND_CHANNEL[DEFAULT_LANG])
        return
    try:
        channel, cr = Channel.objects.get_or_create(chat_id=f"{chat.id}")
        channel.full_name = chat.title
        channel.username = chat.username
        channel.goal = Channel.Goals.send
        if not channel.added_user:
            channel.added_user = user
        channel.save()
    except:
        traceback.print_exc()
        await message.answer(Texts.NOT_ADD_CHANNEL[DEFAULT_LANG])
    else:
        await message.answer(Texts.ADDED_CHANNEL[DEFAULT_LANG], reply_markup=await channels_kb(goal=Channel.Goals.send))
        await state.set_state(MyChannelForm.MyChannel)


@dp.message(F.text.in_(Texts.REMOVE.values()), MyChannelForm.MyChannel)
async def input_channel_for_remove(message: Message, state: FSMContext):
    await message.answer(Texts.INPUT_CHANNEL_FOR_REMOVE[DEFAULT_LANG],
                         reply_markup=await channels_kb(goal=Channel.Goals.send, cancel_kb=True))
    await state.set_state(MyChannelForm.RemoveChannel)


@dp.message(MyChannelForm.RemoveChannel)
async def get_channel_for_remove(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    channel = await get_channel(message.text)
    try:
        if channel:
            channel.added_user = None
            channel.goal = None
            channel.save()
    except:
        await message.answer(Texts.NOT_REMOVE_CHANNEL[DEFAULT_LANG])
    else:
        user.refresh_from_db()
        await message.answer(Texts.REMOVED_CHANNEL[DEFAULT_LANG], reply_markup=await channels_kb(goal=Channel.Goals.send))
        await state.set_state(MyChannelForm.MyChannel)


@dp.message(MyChannelForm.MyChannel)
async def channel_info(message: Message):
    channel = await get_channel(message.text)
    text = (f"♻️ <b>Fullname:</b> <i>{channel.full_name if channel.full_name else '❌'}</i>"
            f"\n👤 <b>Username:</b> <i>{('@' + channel.username) if channel.username else '❌'}</i>"
            f"\n👤 <b>Telegram ID:</b> <i>{channel.chat_id}</i>")
    await message.reply(text)
