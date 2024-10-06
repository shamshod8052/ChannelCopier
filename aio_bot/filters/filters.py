from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from Admin.models import User, Channel


async def get_channel(info):
    name = info[info.find(' ') + 1:]
    name = name.replace('@', '')
    for t in ['username', 'full_name', 'chat_id']:
        my_channels = Channel.objects.filter(**{t: name})
        if my_channels.exists():
            return my_channels.first()
    return None


class IsNotAdminFilter(Filter):
    async def __call__(self, obj) -> bool:
        chat_id = None
        username = None
        full_name = None
        if isinstance(obj, Message):
            chat_id = obj.chat.id
            username = obj.chat.username
            full_name = obj.chat.full_name
        elif isinstance(obj, CallbackQuery):
            chat_id = obj.message.chat.id
            username = obj.message.chat.username
            full_name = obj.message.chat.full_name

        users = User.objects.filter(chat_id=chat_id)
        if not users.exists():
            User.objects.create(chat_id=chat_id, username=username, full_name=full_name)
        return users.exists() and not users.first().is_admin
