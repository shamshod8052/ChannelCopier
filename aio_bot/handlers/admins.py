from typing import Optional

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Admin.models import User, Channel
from aio_bot.buttons import admins_kb, cancel
from aio_bot.config import DEFAULT_LANG
from aio_bot.filters.filters import UserFilter, get_user, IsAdminFilter
from aio_bot.loader import dp
from aio_bot.states import AdminForm
from enums import Texts


@dp.message(IsAdminFilter(), F.text.in_(Texts.ADMINS.values()))
async def my_admins(message: Message, state: FSMContext):
    await state.set_state(AdminForm.Admin)
    user = User.objects.get(chat_id=message.chat.id)
    await message.answer(Texts.YOUR_ADMINS[DEFAULT_LANG], reply_markup=await admins_kb(user))


@dp.message(F.text.in_(Texts.ADD.values()), AdminForm.Admin)
async def add_admin(message: Message, state: FSMContext):
    await message.answer(Texts.SEND_ADMIN[DEFAULT_LANG], reply_markup=await cancel())
    await state.set_state(AdminForm.GetAdmin)


@dp.message(AdminForm.GetAdmin)
async def get_admin_form(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    chat = message.forward_from
    if not chat:
        await message.answer(Texts.NOT_FOUND_ADMIN[DEFAULT_LANG])
        return
    try:
        admin, cr = User.objects.get_or_create(chat_id=chat.id)
        admin.full_name = chat.full_name
        admin.username = chat.username
        admin.save()
        user.admins.add(admin)
        user.refresh_from_db()
        await message.answer(Texts.ADDED_ADMIN[DEFAULT_LANG], reply_markup=await admins_kb(user))
        await state.set_state(AdminForm.Admin)
    except:
        await message.answer(Texts.NOT_ADD_ADMIN[DEFAULT_LANG])


@dp.message(F.text.in_(Texts.REMOVE.values()), AdminForm.Admin)
async def input_admin_for_remove(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    await message.answer(Texts.INPUT_ADMIN_FOR_REMOVE[DEFAULT_LANG],
                         reply_markup=await admins_kb(user, cancel_kb=True))
    await state.set_state(AdminForm.RemoveAdmin)


@dp.message(AdminForm.RemoveAdmin)
async def get_admin_for_remove(message: Message, state: FSMContext):
    user = User.objects.get(chat_id=message.chat.id)
    admin = await get_user(user.admins, message.text)

    try:
        if admin:
            user.admins.remove(admin)
    except:
        await message.answer(Texts.NOT_REMOVE_ADMIN[DEFAULT_LANG])
    else:
        user.refresh_from_db()
        await message.answer(Texts.REMOVED_ADMIN[DEFAULT_LANG], reply_markup=await admins_kb(user))
        await state.set_state(AdminForm.Admin)


@dp.message(AdminForm.Admin, IsAdminFilter(), UserFilter())
async def admin_info(message: Message):
    user = User.objects.get(chat_id=message.chat.id)
    admin: Optional[Channel] = await get_user(user.admins, message.text)
    text = (f"♻️ <b>Fullname:</b> <i>{admin.full_name if admin.full_name else '❌'}</i>"
            f"\n👤 <b>Username:</b> <i>{('@' + admin.username) if admin.username else '❌'}</i>"
            f"\n👤 <b>Telegram ID:</b> <i>{admin.chat_id}</i>")
    await message.reply(text)
