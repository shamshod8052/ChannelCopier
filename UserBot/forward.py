import asyncio
import logging
import traceback

from telethon.errors import MessageEmptyError, MessageNotModifiedError, FloodWaitError

from UserBot.cleaner import Cleaner
from UserBot.functions import add_messages_for_base
from UserBot.loader import client


class Forward:
    def __init__(self, message, chat_id, extra_text: str = ''):
        self.message = message
        self.chat_id = chat_id
        self.extra_text = extra_text

    async def forward(self, chat_id):
        cleaner = Cleaner(
            text=self.message.message,
            entities=self.message.entities,
            extra_text=self.extra_text
        )
        cleaned_text, cleaned_entities = await cleaner.clean_text()

        self.message.message = cleaned_text
        self.message.entities = cleaned_entities

        try:
            sent_message = await client.send_message(chat_id, message=self.message)
            logging.info("Message sent successfully")
            await add_messages_for_base(self.chat_id, chat_id, [self.message], [sent_message])
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await self.forward(chat_id)
        except MessageEmptyError:
            pass
        except MessageNotModifiedError:
            pass
        except:
            traceback.print_exc()
