from telethon.events import NewMessage, MessageEdited, MessageDeleted
from telethon import events

from user_bot.album import MediaGroup
from user_bot.delete import DeleteMessage
from user_bot.edit import EditedMessage
from user_bot.forward import ForwardMessage
from user_bot.loader import client, logger


@client.on(events.Album)
async def handle_media_group(album: events.Album.Event):
    """
    Handles media group (album) events.
    Forwards the album to the destination chat using the MediaGroup class.
    """
    try:
        logger.info(f"Received media group with ID: {album.messages[0].grouped_id} from chat: {album.chat_id}")
        await MediaGroup(album, album.messages).send_media_group()
        logger.info(f"Successfully forwarded media group {album.messages[0].grouped_id}")
    except Exception as e:
        logger.error(f"Error forwarding media group: {e}", exc_info=True)


@client.on(NewMessage)
async def handle_new_message(event: NewMessage.Event):
    """
    Handles new messages.
    Forwards the message if it's not part of a media group (album).
    """
    try:
        if not event.message.grouped_id:
            logger.info(f"New message from chat {event.chat_id}, message ID: {event.message.id}")
            await ForwardMessage(event).forward()
            logger.info(f"Successfully forwarded message {event.message.id}")
        else:
            logger.info(f"Message {event.message.id} is part of a media group, skipping individual forwarding.")
    except Exception as e:
        logger.error(f"Error forwarding message {event.message.id}: {e}", exc_info=True)


@client.on(MessageEdited)
async def handle_edited_message(event: MessageEdited.Event):
    """
    Handles message edits.
    Updates the message in the destination chat using the EditedMessage class.
    """
    try:
        logger.info(f"Message edited in chat {event.chat_id}, message ID: {event.message.id}")
        await EditedMessage(event).edit()
        logger.info(f"Successfully edited message {event.message.id}")
    except Exception as e:
        logger.error(f"Error editing message {event.message.id}: {e}", exc_info=True)


@client.on(MessageDeleted)
async def handle_deleted_message(event: MessageDeleted.Event):
    """
    Handles message deletions.
    Deletes the message from the destination chat using the DeleteMessage class.
    """
    try:
        logger.info(f"Message deleted in chat {event.chat_id}, message IDs: {event.deleted_ids}")
        await DeleteMessage(event).delete()
        logger.info(f"Successfully deleted messages {event.deleted_ids}")
    except Exception as e:
        logger.error(f"Error deleting messages {event.deleted_ids}: {e}", exc_info=True)
