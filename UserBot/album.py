import asyncio
import logging
import traceback
from typing import List, Optional
from telethon.tl.types import Message as TeleMessage

from telethon.errors import FloodWaitError
from telethon.extensions import markdown

from UserBot.cleaner import Cleaner
from UserBot.functions import add_messages_for_base
from UserBot.loader import client


class MyAlbum:
    def __init__(self, messages: Optional[List[TeleMessage]] = None, extra_text: str = ''):
        if messages is None:
            messages = []
        self.messages = messages
        self.chat_id = self.messages[0].chat_id
        self.posts = None
        self.extra_text = extra_text

    @staticmethod
    async def get_media_posts_in_group(chat_id, original_post, max_amp=10) -> list:
        if original_post.grouped_id is None:
            return [original_post] if original_post.media is not None else []

        search_ids = [i for i in range(original_post.id - max_amp, original_post.id + max_amp + 1)]
        posts = await client.get_messages(chat_id, ids=search_ids)
        media = []
        for post in posts:
            if post is not None and post.grouped_id == original_post.grouped_id and post.media is not None:
                media.append(post)
        return media

    async def generate_posts(self):
        if not self.posts:
            self.posts = await self.get_media_posts_in_group(self.chat_id, self.messages[0])

    async def media_list_parsing(self):
        media, force_document = [], False
        for group_message in self.posts:
            if group_message.photo:
                media.append(group_message.photo)
            elif group_message.video:
                media.append(group_message.video)
            elif group_message.document:
                media.append(group_message.document)
                force_document = True

        return dict(
            file=media, force_document=force_document
        )

    async def caption_parsing(self):
        cleaned_text, cleaned_entities = None, None
        for message in self.posts:
            if message.message:
                cleaner = Cleaner(
                    text=message.message, entities=message.entities, extra_text=self.extra_text
                )
                cleaned_text, cleaned_entities = await cleaner.clean_text()
                break
        caption = markdown.unparse(cleaned_text, cleaned_entities)

        return caption

    async def send_album(self, chat_id):
        await self.generate_posts()
        if not self.posts:
            logging.info("Posts list is empty for album")
            return
        media_info = await self.media_list_parsing()
        caption = await self.caption_parsing()
        try:
            sent_messages = await client.send_file(
                entity=chat_id, caption=caption, **media_info
            )
            logging.info("Album sent successfully")
            await add_messages_for_base(self.chat_id, chat_id, self.posts, sent_messages)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await self.send_album(chat_id)
        except:
            traceback.print_exc()
