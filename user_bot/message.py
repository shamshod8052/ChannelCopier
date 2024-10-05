from django.db.models import Q

from Admin.models import Channel, User, Message


async def get_channel(chat_id):
    try:
        return Channel.objects.get(chat_id=chat_id)
    except Channel.DoesNotExist:
        return None


async def get_send_chat_id(channel):
    if not (channel.users.exists() and (channel.users.first().is_admin or channel.users.first().boss.exists())):
        return None

    admin_users = User.objects.filter(~Q(channel_for_send=None), is_admin=True)
    if not admin_users.exists():
        return None

    return int(admin_users.first().channel_for_send.chat_id)


async def get_message_obj(chat_id, message_ids):
    try:
        return Message.objects.get(from_chat_id=chat_id, from_message_ids__contains=message_ids)
    except Message.DoesNotExist:
        return None
