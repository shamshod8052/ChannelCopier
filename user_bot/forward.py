import asyncio

from telethon.errors import MessageEmptyError

from Admin.models import Message
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner
from user_bot.loader import client


class ForwardMessage(MyMessage):
    media_groups = {}

    def __init__(self, event):
        super().__init__(event)
        self.send_chat_id = None

    async def forward(self):
        channel = await self._get_channel(self.event.message.chat_id)
        if not channel:
            return

        self.send_chat_id = await self._get_send_chat_id(channel)
        if not self.send_chat_id:
            return

        if self.event.message.grouped_id:  # Handle media group messages
            from_msgs, to_msgs = await self.media_group()
        else:
            from_msgs, to_msgs = await self._forward_single_message(self.send_chat_id)
        if not from_msgs or not to_msgs:
            return
        from_message_ids = [m.id for m in from_msgs]
        to_message_ids = [m.id for m in to_msgs]
        Message.objects.get_or_create(from_chat_id=self.event.chat_id, from_message_ids=from_message_ids,
                                      to_chat_id=self.send_chat_id, to_message_ids=to_message_ids)

    async def media_group(self):
        grouped_id = self.event.message.grouped_id
        media_group = self.media_groups.setdefault(grouped_id, {'messages': [], 'message_ids': []})

        media_group['messages'].append(self.event.message)
        media_group['message_ids'].append(self.event.message.id)

        if self.event.message.message:
            media_group.setdefault('text', self.event.message.message)

        await asyncio.sleep(3)

        if self.event.message.id == media_group['message_ids'][0]:
            old_msgs, new_msgs = await self._send_media_group(media_group)
            return old_msgs, new_msgs
        else:
            return [], []

    async def _send_media_group(self, media_group):
        from_msgs = media_group['messages']
        text = media_group.get('text', '')
        caption = await TextCleaner.clean_text(text, self.event.message.entities)
        to_msgs = await client.send_file(self.send_chat_id, file=from_msgs, caption=caption)

        return from_msgs, to_msgs

    async def _forward_single_message(self, send_chat_id):
        helper_msg = self.event.message
        helper_msg.message = await TextCleaner.clean_text(helper_msg.message, helper_msg.entities)
        try:
            msg = await client.send_message(send_chat_id, message=helper_msg)
            return [self.event.message], [msg]
        except MessageEmptyError:
            pass
