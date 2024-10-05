from telethon.sync import events

from Admin.models import Message
from user_bot.loader import client
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner


class MediaGroup(events.Album):
    def __init__(self, album):
        super().__init__()
        self.album = album
        self.send_chat_id = None

    async def send_media_group(self):
        channel = await MyMessage.get_channel(self.album.messages[0].chat_id)
        if not channel:
            return

        self.send_chat_id = await MyMessage.get_send_chat_id(channel)
        if not self.send_chat_id:
            return

        from_msgs, to_msgs = await self._send_media_group()

        if not from_msgs or not to_msgs:
            return

        from_message_ids = [m.id for m in from_msgs]
        to_message_ids = [m.id for m in to_msgs]
        Message.objects.get_or_create(
            from_chat_id=self.album.messages[0].chat_id, from_message_ids=from_message_ids,
            to_chat_id=self.send_chat_id, to_message_ids=to_message_ids
        )

    async def _send_media_group(self):
        messages = self.album.messages
        text = self.album.messages[0].text
        entities = self.album.messages[0].entities
        caption = await TextCleaner.clean_text(text, entities)
        to_msgs = await client.send_file(self.send_chat_id, file=messages, caption=caption)
        return messages, to_msgs
