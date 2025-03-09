import asyncio
import logging
from typing import List

from telethon.tl.types import Message as TeleMessage

from Admin.models import User, Sender, Getter
from UserBot.album import MyAlbum
from UserBot.forward import Forward
from UserBot.loader import client


async def mailing_manager(sender_msg: TeleMessage, sender: Sender, getter: Getter):
    logging.info("Mailing manager running")
    if sender_msg.grouped_id:
        album = MyAlbum([sender_msg], getter.user.extra_text)
        await album.send_album(getter.channel.chat_id)
    else:
        fwd = Forward(sender_msg, sender.channel.chat_id, getter.user.extra_text)
        await fwd.forward(getter.channel.chat_id)


async def getter_manager(messages: List[TeleMessage], sender: Sender, getter: Getter):
    logging.info(f"Running {len(messages)} getter manager tasks ")

    for sender_msg in messages:
        await mailing_manager(sender_msg, sender, getter)


async def sender_manager(sender: Sender):
    messages = await sender.channel.get_free_messages_group(client)
    getters = sender.user.getters.all()
    logging.info("Sender manager running")
    logging.info(f"{len(messages)} messages found")

    tasks = [
        getter_manager(messages, sender, getter)
        for getter in getters
        if sender.channel != getter.channel
    ]
    logging.info(f"Running {len(tasks)} sender manager tasks ")

    await asyncio.gather(*tasks)


async def user_manager(user: User):
    """Checks whether channel messages for a given user have been copied."""
    logging.info("User manager running")
    tasks = [
        sender_manager(sender) for sender in user.senders.all()
    ]
    logging.info(f"Running {len(tasks)} user manager tasks ")

    await asyncio.gather(*tasks)


async def copy_manager():
    """Creates a task that copies messages for each user"""
    logging.info("Copying manager running")
    tasks = [
        user_manager(user) for user in User.objects.filter(process_status=True).all()
    ]
    logging.info(f"Running {len(tasks)} copy manager tasks ")

    await asyncio.gather(*tasks)
