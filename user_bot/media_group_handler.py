import asyncio
from user_bot.text_cleaner import TextCleaner
from user_bot.loader import client


class MediaGroupHandler:
    """
    Handles media groups in messages.
    Collects and sends grouped media messages as a batch.
    """
    media_groups = {}

    def __init__(self, event, send_chat_id):
        self.event = event
        self.send_chat_id = send_chat_id

    async def handle(self):
        """
        Handle a media group message. Collect all messages in the group and send them after a delay.

        :return: None
        """
        grouped_id = self.event.message.grouped_id
        media_group = MediaGroupHandler.media_groups.setdefault(grouped_id, {'messages': [], 'message_ids': []})

        media_group['messages'].append(self.event.message)
        media_group['message_ids'].append(self.event.message.id)

        if self.event.message.message:
            media_group.setdefault('text', self.event.message.message)

        await asyncio.sleep(3)

        if self.event.message.id == media_group['message_ids'][0]:
            msgs = await self._send_media_group(media_group)
            return msgs[0]

    async def _send_media_group(self, media_group):
        """
        Send the collected media group to the specified chat.

        :param media_group: Collected media messages in the group.
        :return: None
        """
        messages = media_group['messages']
        text = media_group.get('text', '')
        caption = await TextCleaner.clean_text(text, self.event.message.entities)
        msg = await client.send_file(self.send_chat_id, file=messages, caption=caption)

        return msg
