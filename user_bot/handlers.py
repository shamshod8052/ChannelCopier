from telethon.events import NewMessage, MessageEdited, MessageDeleted

from user_bot.delete import DeleteMessage
from user_bot.edit import EditedMessage
from user_bot.forward import ForwardMessage
from user_bot.loader import client


@client.on(NewMessage)
async def handle_new_message(event: NewMessage.Event):
    await ForwardMessage(event).forward()


@client.on(MessageEdited)
async def handle_edited_message(event: MessageEdited.Event):
    await EditedMessage(event).edit()


@client.on(MessageDeleted)
async def handle_deleted_message(event: MessageDeleted.Event):
    await DeleteMessage(event).delete()
