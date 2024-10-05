from telethon import events

from Admin.models import Message
from user_bot.loader import client, logger
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner


class MediaGroup(events.Album.Event):
    def __init__(self, album, messages):
        super().__init__(messages)
        self.album = album
        self.send_chat_id = None

        self.posts = []

    @staticmethod
    async def _get_media_posts_in_group(chat, original_post, max_amp=10) -> list:
        """
        Searches for Telegram posts that are part of the same group of uploads
        The search is conducted around the id of the original post with an amplitude
        of `max_amp` both ways
        Returns a list of [post] where each post has media and is in the same grouped_id
        """
        if original_post.grouped_id is None:
            return [original_post] if original_post.media is not None else []

        search_ids = [i for i in range(original_post.id - max_amp, original_post.id + max_amp + 1)]
        posts = await client.get_messages(chat, ids=search_ids)
        media = []
        for post in posts:
            if post is not None and post.grouped_id == original_post.grouped_id and post.media is not None:
                media.append(post)
        return media

    async def send_media_group(self):
        channel = await MyMessage.get_channel(self.messages[0].chat_id)
        print(self.messages[0].chat_id)
        if not channel:
            return

        self.send_chat_id = await MyMessage.get_send_chat_id(channel)
        if not self.send_chat_id:
            return

        self.posts = await self._get_media_posts_in_group(self.messages[0].chat_id, self.messages[0])
        from_msgs, to_msgs = await self._send_media_group()

        if not from_msgs or not to_msgs:
            return

        from_message_ids = [m.id for m in from_msgs]
        to_message_ids = [m.id for m in to_msgs]
        Message.objects.get_or_create(
            from_chat_id=self.posts[0].chat_id, from_message_ids=from_message_ids,
            to_chat_id=self.send_chat_id, to_message_ids=to_message_ids
        )

    async def _send_media_group(self):
        caption = None
        posts = self.posts
        for message in posts:
            if message.text:
                caption = await TextCleaner.clean_text(message.text, message.entities)
                break
        if not caption:
            logger.info(f"caption is None. chat_id: {self.messages[0].chat_id}, msg_id: {self.messages[0].id}")

        to_msgs = await client.send_file(self.send_chat_id, file=posts, caption=caption)
        return posts, to_msgs
