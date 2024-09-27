from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Admin.models import User, Channel
from aio_bot.buttons import menu, channels_kb, cancel
from aio_bot.config import DEFAULT_LANG
from aio_bot.loader import dp
from aio_bot.states import UserForm
from enums import Texts


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    user, cr = User.objects.get_or_create(chat_id=message.chat.id)
    user.full_name = message.chat.full_name
    user.username = message.chat.username
    user.save()
    await state.set_state(None)
    await message.answer(Texts.HELLO[DEFAULT_LANG] + ' ' + message.from_user.full_name, reply_markup=await menu())


@dp.message(F.text.in_(Texts.CANCEL.values()))
@dp.message(F.text.in_(Texts.CHANNELS.values()))
async def my_channels(message: Message, state: FSMContext):
    await state.set_state(None)
    user = User.objects.get(chat_id=message.chat.id)
    await message.answer(Texts.YOUR_CHANNELS[DEFAULT_LANG], reply_markup=await channels_kb(user))


@dp.message(F.text.in_(Texts.ADD.values()))
async def add_channel(message: Message, state: FSMContext):
    await message.answer(Texts.SEND_CHANNEL[DEFAULT_LANG], reply_markup=await cancel())
    await state.set_state(UserForm.GetChannel)


@dp.message(UserForm.GetChannel)
async def get_channel(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    chat = message.forward_from_chat
    if not chat:
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
        await state.set_state(None)
    except:
        await message.answer(Texts.NOT_ADD_CHANNEL[DEFAULT_LANG])


@dp.message(F.text.in_(Texts.REMOVE.values()))
async def input_channel_for_remove(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    await message.answer(Texts.INPUT_CHANNEL_FOR_REMOVE[DEFAULT_LANG],
                         reply_markup=await channels_kb(user, cancel_kb=True))
    await state.set_state(UserForm.RemoveChannel)


@dp.message(UserForm.RemoveChannel)
async def get_channel_for_remove(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    for t in ['full_name', 'username', 'chat_id']:
        kwargs = {t: message.text[message.text.find(' ') + 1:]}
        try:
            channel = Channel.objects.get(**kwargs)
            break
        except:
            channel = None

    try:
        if channel:
            channel.delete()
    except:
        await message.answer(Texts.NOT_REMOVE_CHANNEL[DEFAULT_LANG])
    else:
        user.refresh_from_db()
        await message.answer(Texts.REMOVED_CHANNEL[DEFAULT_LANG], reply_markup=await channels_kb(user))
        await state.set_state(None)


@dp.message()
async def echo_(message: Message):
    await message.reply(Texts.SELECT_MENUS[DEFAULT_LANG])
