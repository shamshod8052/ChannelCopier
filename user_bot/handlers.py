from telethon.events import NewMessage, MessageEdited

from user_bot.edited_msg_handler import EditedMessageHandler
from user_bot.loader import client
from user_bot.message_handler import NewMessageHandler


@client.on(NewMessage)
async def handle_new_message(event: NewMessage.Event):
    await NewMessageHandler(event).process_message()


@client.on(MessageEdited)
async def handle_edited_message(event: MessageEdited.Event):
    await EditedMessageHandler(event).process_message()
