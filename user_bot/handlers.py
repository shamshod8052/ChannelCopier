import logging
from telethon.events import NewMessage, MessageEdited, MessageDeleted

from user_bot.delete import DeleteMessage
from user_bot.edit import EditedMessage
from user_bot.forward import ForwardMessage
from user_bot.loader import client


@client.on(NewMessage)
async def handle_new_message(event: NewMessage.Event):
    try:
        await ForwardMessage(event).forward()
        logging.info(f"New message forwarded from chat {event.message.chat_id}.")
    except Exception as e:
        logging.error(f"Error handling new message: {e}")


@client.on(MessageEdited)
async def handle_edited_message(event: MessageEdited.Event):
    try:
        await EditedMessage(event).edit()
        logging.info(f"Message edited in chat {event.message.chat_id}.")
    except Exception as e:
        logging.error(f"Error handling edited message: {e}")


@client.on(MessageDeleted)
async def handle_deleted_message(event: MessageDeleted.Event):
    try:
        await DeleteMessage(event).delete()
        logging.info(f"Message deleted in chat {event.chat_id}.")
    except Exception as e:
        logging.error(f"Error handling deleted message: {e}")
