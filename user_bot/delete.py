import asyncio

from user_bot.config import SLEEP_TIME_EDIT
from user_bot.loader import client
from user_bot.message import get_message_obj


async def delete_single_message(to_chat_id, to_message_ids):
    try:
        await client.delete_messages(to_chat_id, to_message_ids)
    except Exception as e:
        ...


async def delete(event):
    await asyncio.sleep(SLEEP_TIME_EDIT)
    chat_id = event.chat_id
    message_obj = await get_message_obj(chat_id, event.deleted_ids)
    if not message_obj:
        return
    print(event)
    to_chat_id = int(message_obj.to_chat_id)
    to_message_ids = []

    for from_id in event.deleted_ids:
        try:
            from_index = message_obj.from_message_ids.index(from_id)
            del message_obj.from_message_ids[from_index]
            to_message_ids.append(message_obj.to_message_ids.pop(from_index))
        except ValueError:
            continue

    message_obj.save()

    if to_chat_id and to_message_ids:
        await delete_single_message(to_chat_id, to_message_ids)
