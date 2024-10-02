from django.db.models import Q

from Admin.models import Channel, User, Message


class MyMessage:
    def __init__(self, event):
        self.event = event

    @staticmethod
    async def _get_channel(chat_id):
        try:
            return Channel.objects.get(chat_id=chat_id)
        except Channel.DoesNotExist:
            return None

    @staticmethod
    async def _get_send_chat_id(channel):
        if not (channel.users.exists() and (channel.users.first().is_admin or channel.users.first().boss.exists())):
            return None

        admin_users = User.objects.filter(~Q(channel_for_send=None), is_admin=True)
        if not admin_users.exists():
            return None

        return int(admin_users.first().channel_for_send.chat_id)

    async def _get_message_obj(self, message_ids):
        try:
            return Message.objects.get(from_chat_id=self.event.chat_id, from_message_ids__contains=message_ids)
        except Message.DoesNotExist:
            return None
