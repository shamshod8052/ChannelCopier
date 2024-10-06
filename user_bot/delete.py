import asyncio

from user_bot.config import SLEEP_TIME_EDIT
from user_bot.loader import client
from user_bot.message import get_message_objs


async def delete_messages(to_chat_id, to_message_ids):
    try:
        await client.delete_messages(to_chat_id, to_message_ids)
    except Exception as e:
        ...


async def delete(event):
    await asyncio.sleep(SLEEP_TIME_EDIT)
    chat_id = event.chat_id
    message_objs = await get_message_objs(chat_id, event.deleted_ids)
    if not message_objs:
        return
    print(event)
    for msg_obj in message_objs:
        to_chat_id = int(msg_obj.to_chat_id)
        to_message_ids = []

        for from_id in event.deleted_ids:
            try:
                from_index = msg_obj.from_message_ids.index(from_id)
                del msg_obj.from_message_ids[from_index]
                to_message_ids.append(msg_obj.to_message_ids.pop(from_index))
            except ValueError:
                continue

        msg_obj.save()

        if to_chat_id and to_message_ids:
            await delete_messages(to_chat_id, to_message_ids)
