from telethon.errors import MessageEmptyError

from Admin.models import Message
from user_bot.loader import client
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner


class ForwardMessage(MyMessage):
    """Class to handle forwarding of messages or media groups."""

    def __init__(self, event):
        super().__init__(event)
        self.send_chat_id = None

    async def forward(self):
        """Forward the message to another chat."""
        channel = await self.get_channel(self.event.message.chat_id)
        if not channel:
            return

        self.send_chat_id = await self.get_send_chat_id(channel)
        if not self.send_chat_id:
            return

        # Single message forwarding
        from_msgs, to_msgs = await self._forward_single_message()

        if not from_msgs or not to_msgs:
            return

        from_message_ids = [m.id for m in from_msgs]
        to_message_ids = [m.id for m in to_msgs]
        Message.objects.get_or_create(
            from_chat_id=self.event.chat_id, from_message_ids=from_message_ids,
            to_chat_id=self.send_chat_id, to_message_ids=to_message_ids
        )

    async def _forward_single_message(self):
        """Forward a single message."""
        helper_msg = self.event.message
        helper_msg.message = await TextCleaner.clean_text(helper_msg.message, helper_msg.entities)

        try:
            msg = await client.send_message(self.send_chat_id, message=helper_msg)
            return [self.event.message], [msg]
        except MessageEmptyError:
            return [], []
