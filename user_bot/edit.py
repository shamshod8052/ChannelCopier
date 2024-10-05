import asyncio

from telethon.errors.rpcerrorlist import MessageNotModifiedError

from user_bot.config import SLEEP_TIME_EDIT
from user_bot.loader import client
from user_bot.message import get_message_obj
from user_bot.text_cleaner import clean_text


async def edit_single_message(event, to_chat_id, to_message_id):
    try:
        helper_msg = event.message

        text = await clean_text(helper_msg.message, helper_msg.entities)
        helper_msg.message = text

        await client.edit_message(
            to_chat_id,
            message=to_message_id,
            text=text,
            file=helper_msg,
            parse_mode='markdown'
        )
    except MessageNotModifiedError:
        pass
    except Exception as e:
        print(f"Error editing message: {e}")


async def edit(event):
    await asyncio.sleep(SLEEP_TIME_EDIT)
    message_obj = await get_message_obj(event.chat_id, [event.message.id])
    if not message_obj:
        return
    print(event)
    to_chat_id = int(message_obj.to_chat_id)

    try:
        from_index = message_obj.from_message_ids.index(event.message.id)
        to_message_id = message_obj.to_message_ids[from_index]
    except (ValueError, IndexError):
        return

    if to_chat_id and to_message_id:
        await edit_single_message(event, to_chat_id, to_message_id)
