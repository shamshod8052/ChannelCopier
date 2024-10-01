from user_bot.media_group_handler import MediaGroupHandler
from user_bot.text_cleaner import TextCleaner
from Admin.models import Channel, User, Message
from django.db.models import Q
from telethon.errors.rpcerrorlist import MessageEmptyError
from user_bot.loader import client


class NewMessageHandler:
    """
    Main message handler that processes incoming messages and routes them appropriately.
    """

    def __init__(self, event):
        self.event = event

    async def process_message(self):
        """
        Process the incoming message by checking if it's part of a media group or a single message.

        :return: None
        """
        channel = await self._get_channel()
        if not channel:
            return

        send_chat_id = await self._get_send_chat_id(channel)
        if not send_chat_id:
            return

        if self.event.message.grouped_id:  # Handle media group messages
            msg = await MediaGroupHandler(self.event, send_chat_id).handle()
        else:
            msg = await self._send_single_message(send_chat_id)
        if not msg:
            return
        Message.objects.create(from_chat_id=self.event.chat_id, from_message_id=self.event.message.id,
                               to_chat_id=send_chat_id, to_message_id=msg.id)

    async def _get_channel(self):
        """
        Retrieve the channel from the database based on the chat ID in the event.

        :return: Channel object or None if the channel doesn't exist.
        """
        try:
            return Channel.objects.get(chat_id=self.event.chat_id)
        except Channel.DoesNotExist:
            return None

    @staticmethod
    async def _get_send_chat_id(channel):
        """
        Get the chat ID where messages should be forwarded.

        :param channel: The channel to check for the send chat ID.
        :return: The send chat ID or None if no suitable chat is found.
        """
        if not (channel.users.exists() and (channel.users.first().is_admin or channel.users.first().boss.exists())):
            return None

        admin_users = User.objects.filter(~Q(channel_for_send=None), is_admin=True)
        if not admin_users.exists():
            return None

        return int(admin_users.first().channel_for_send.chat_id)

    async def _send_single_message(self, send_chat_id):
        """
        Clean and send a single message.

        :param send_chat_id: Chat ID to send the message to.
        :return: None
        """
        msg = self.event.message
        msg.message = await TextCleaner.clean_text(msg.message, msg.entities)
        try:
            msg = await client.send_message(send_chat_id, message=msg)
            return msg
        except MessageEmptyError:
            pass
