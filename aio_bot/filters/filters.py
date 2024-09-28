from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from Admin.models import Channel, User


async def get_channel(channels, info):
    info = info[info.find(' ') + 1:]
    info = info.replace('@', '')
    for t in ['username', 'full_name', 'chat_id']:
        try:
            my_channels = channels.filter(**{t: info})
        except Channel.DoesNotExist:
            ...
        else:
            if my_channels.exists():
                return my_channels.first()
    return None


async def get_user(admins, info):
    info = info[info.find(' ') + 1:]
    info = info.replace('@', '')
    for t in ['username', 'full_name', 'chat_id']:
        try:
            my_admins = admins.filter(**{t: info})
        except User.DoesNotExist:
            ...
        else:
            if my_admins.exists():
                return my_admins.first()
    return None


class IsHaveChannelFilter(Filter):
    async def __call__(self, obj) -> bool:
        if isinstance(obj, Message):
            user = User.objects.get(chat_id=obj.chat.id)
            channel = await get_channel(user.channels, obj.text)
            return channel is not None
        return False


class UserFilter(Filter):
    async def __call__(self, obj) -> bool:
        if isinstance(obj, Message):
            user = User.objects.get(chat_id=obj.chat.id)
            admin = await get_user(user.admins, obj.text)
            return admin is not None
        return False


class IsHaveBossFilter(Filter):
    async def __call__(self, obj) -> bool:
        chat_id = None
        if isinstance(obj, Message):
            chat_id = obj.chat.id
        elif isinstance(obj, CallbackQuery):
            chat_id = obj.message.chat.id

        users = User.objects.filter(chat_id=chat_id)
        return users.exists() and users.first().boss.exists()


class IsAdminFilter(Filter):
    async def __call__(self, obj) -> bool:
        chat_id = None
        if isinstance(obj, Message):
            chat_id = obj.chat.id
        elif isinstance(obj, CallbackQuery):
            chat_id = obj.message.chat.id

        users = User.objects.filter(chat_id=chat_id)
        return users.exists() and users.first().is_admin
