from telethon.events import MessageEdited, MessageDeleted, StopPropagation

from UserBot.loader import client


@client.on(MessageEdited)
async def handle_edited_message(event: MessageEdited.Event):
    # await Edit(event).edit()

    raise StopPropagation


@client.on(MessageDeleted)
async def handle_deleted_message(event: MessageDeleted.Event):
#     await Delete(event).delete()

    raise StopPropagation
