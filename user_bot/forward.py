import asyncio
from telethon.errors import MessageEmptyError
from telethon.events import NewMessage
from Admin.models import Message
from user_bot.config import SLEEP_TIME_MEDIA_GROUP
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner
from user_bot.loader import client


class MediaGroupMessage:
    _media_groups = {}

    def __init__(self, event):
        self.event: NewMessage.Event = event

    @property
    def media_groups(self) -> dict:
        return MediaGroupMessage._media_groups

    def add_message(self):
        group_id = self.event.message.grouped_id
        message_id = self.event.message.id
        chat_id = self.event.chat_id

        key = f"{group_id}:{message_id}:{chat_id}"
        message = self.event.message
        self.media_groups[key] = message

    def pop_message(self, key):
        return self.media_groups.pop(key, None)

    def remove_messages_list(self):
        """Removes all messages in a group once they are sent."""
        my_group_id = str(self.event.message.grouped_id)
        my_chat_id = str(self.event.chat_id)
        media_groups = self.media_groups.copy()

        for key in list(media_groups.keys()):
            group_id, message_id, chat_id = key.split(':')
            if my_group_id == group_id and my_chat_id == chat_id:
                self.pop_message(key)

    def get_messages_list(self):
        """Returns all messages belonging to the same media group."""
        my_group_id = str(self.event.message.grouped_id)
        my_chat_id = str(self.event.chat_id)
        messages = []
        caption = ''
        media_groups = self.media_groups.copy()

        for key, message in media_groups.items():
            group_id, message_id, chat_id = key.split(':')
            if my_group_id == group_id and my_chat_id == chat_id:
                messages.append(message)
                # Retain the first non-empty caption if present
                if not caption and message.message:
                    caption = message.message

        return messages, caption


class ForwardMessage(MyMessage):
    """Class to handle forwarding of messages or media groups."""

    def __init__(self, event):
        super().__init__(event)
        self.send_chat_id = None

    async def forward(self):
        """Forward the message to another chat."""
        channel = await self._get_channel(self.event.message.chat_id)
        if not channel:
            return

        self.send_chat_id = await self._get_send_chat_id(channel)
        if not self.send_chat_id:
            return

        if self.event.message.grouped_id:
            # Media group handling
            from_msgs, to_msgs = await self.media_group()
        else:
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

    async def media_group(self):
        """Handle forwarding of media group messages."""
        mgm = MediaGroupMessage(self.event)
        mgm.add_message()

        # Dynamically wait for all parts of the media group to be received
        await asyncio.sleep(SLEEP_TIME_MEDIA_GROUP)

        messages, caption = mgm.get_messages_list()

        # Only send the group when the last message in the group is received
        if self.event.message.id == messages[-1].id:
            mgm.remove_messages_list()
            return await self._send_media_group(messages, caption)
        else:
            return [], []

    async def _send_media_group(self, messages, caption):
        """Send media group with proper handling of caption."""
        caption = await TextCleaner.clean_text(caption, self.event.message.entities)
        to_msgs = await client.send_file(self.send_chat_id, file=messages, caption=caption)
        return messages, to_msgs

    async def _forward_single_message(self):
        """Forward a single message."""
        helper_msg = self.event.message
        helper_msg.message = await TextCleaner.clean_text(helper_msg.message, helper_msg.entities)

        try:
            msg = await client.send_message(self.send_chat_id, message=helper_msg)
            return [self.event.message], [msg]
        except MessageEmptyError:
            return [], []
