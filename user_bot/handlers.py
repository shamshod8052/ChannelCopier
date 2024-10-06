from telethon.events import NewMessage, MessageEdited, MessageDeleted, Album, Raw

from user_bot.album import send_media_group
from user_bot.delete import delete
from user_bot.edit import edit
from user_bot.forward import forward
from user_bot.loader import client


@client.on(Album)
async def handle_media_group(album: Album.Event):
    print(album)
    await send_media_group(album)


@client.on(NewMessage)
async def handle_new_message(event: NewMessage.Event):
    print(event)
    if not event.message.grouped_id:
        await forward(event)


@client.on(MessageEdited)
async def handle_edited_message(event: MessageEdited.Event):
    print(event)
    await edit(event)


@client.on(MessageDeleted)
async def handle_deleted_message(event: MessageDeleted.Event):
    print(event)
    await delete(event)


@client.on(Raw)
async def handle_raw_event(event):
    print(event)
