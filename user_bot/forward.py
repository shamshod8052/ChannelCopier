import asyncio
from telethon.errors import MessageEmptyError
from Admin.models import Message
from user_bot.config import SLEEP_TIME_MEDIA_GROUP
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner
from user_bot.loader import client


class ForwardMessage(MyMessage):
    """
    Class to handle forwarding messages or media groups, with text cleaning and
    maintaining message history in the database.
    """
    media_groups = {}

    def __init__(self, event):
        super().__init__(event)
        self.send_chat_id = None

    async def forward(self):
        """
        Main method to forward a message or media group. Retrieves the channel, cleans the text,
        and sends the message to the designated chat.
        """
        # Retrieve the destination channel
        channel = await self._get_channel(self.event.message.chat_id)
        if not channel:
            return

        # Get the chat ID to forward to
        self.send_chat_id = await self._get_send_chat_id(channel)
        if not self.send_chat_id:
            return

        # Handle media groups or single messages
        if self.event.message.grouped_id:
            from_msgs, to_msgs = await self.media_group()
        else:
            from_msgs, to_msgs = await self._forward_single_message()

        if not from_msgs or not to_msgs:
            return

        # Store the forwarded messages in the database
        from_message_ids = [m.id for m in from_msgs]
        to_message_ids = [m.id for m in to_msgs]
        Message.objects.get_or_create(
            from_chat_id=self.event.chat_id, from_message_ids=from_message_ids,
            to_chat_id=self.send_chat_id, to_message_ids=to_message_ids
        )

    async def media_group(self):
        """
        Handle forwarding of media group messages (e.g., media albums).

        :return: A tuple of (from_msgs, to_msgs) after forwarding the media group.
        """
        grouped_id = self.event.message.grouped_id
        media_group = self.media_groups.setdefault(grouped_id, {'messages': [], 'message_ids': []})

        # Collect the media group messages
        media_group['messages'].append(self.event.message)
        media_group['message_ids'].append(self.event.message.id)

        # Capture any associated text (if available)
        if self.event.message.message:
            media_group.setdefault('text', self.event.message.message)

        # Wait briefly to ensure the media group is complete
        await asyncio.sleep(SLEEP_TIME_MEDIA_GROUP)

        # Send the media group if this is the first message in the group
        if self.event.message.id == media_group['message_ids'][0]:
            return await self._send_media_group(media_group)
        else:
            return [], []

    async def _send_media_group(self, media_group):
        """
        Sends the collected media group to the destination chat.

        :param media_group: Dictionary containing media group information.
        :return: A tuple of (from_msgs, to_msgs) after sending.
        """
        from_msgs = media_group['messages']
        text = media_group.get('text', '')
        caption = await TextCleaner.clean_text(text, self.event.message.entities)
        # Forward the media group with cleaned caption
        to_msgs = await client.send_file(self.send_chat_id, file=from_msgs, caption=caption)

        return from_msgs, to_msgs

    async def _forward_single_message(self):
        """
        Forwards a single message to the destination chat after cleaning the text.

        :return: A tuple of (from_msgs, to_msgs) after forwarding the single message.
        """
        helper_msg = self.event.message
        helper_msg.message = await TextCleaner.clean_text(helper_msg.message, helper_msg.entities)

        try:
            msg = await client.send_message(self.send_chat_id, message=helper_msg)
            return [self.event.message], [msg]
        except MessageEmptyError:
            # Handle empty message error, which may occur if there's no valid content in the message
            return [], []
