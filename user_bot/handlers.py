from telethon.events import NewMessage, MessageEdited, MessageDeleted, Album

from user_bot.album import send_media_group
from user_bot.delete import delete
from user_bot.edit import edit
from user_bot.forward import forward
from user_bot.loader import client


@client.on(Album)
async def handle_media_group(album: Album.Event):
    await send_media_group(album)


@client.on(NewMessage)
async def handle_new_message(event: NewMessage.Event):
    if not event.message.grouped_id:
        await forward(event)


@client.on(MessageEdited)
async def handle_edited_message(event: MessageEdited.Event):
    await edit(event)


@client.on(MessageDeleted)
async def handle_deleted_message(event: MessageDeleted.Event):
    await delete(event)
