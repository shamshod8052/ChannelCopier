import asyncio

from telethon.errors.rpcerrorlist import MessageNotModifiedError

from user_bot.config import SLEEP_TIME_EDIT
from user_bot.loader import client
from user_bot.message import get_message_objs
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
        print("✅ Message edited successfully", event)
    except MessageNotModifiedError:
        print("MessageNotModifiedError", event)
    except Exception as e:
        print(f"Error editing message: {e}", event)


async def edit(event):
    await asyncio.sleep(SLEEP_TIME_EDIT)
    message_objs = await get_message_objs(event.chat_id, [event.message.id])
    if not message_objs:
        print("Message obj not found", event)
        return
    for msg_obj in message_objs:
        to_chat_id = int(msg_obj.to_chat_id)

        try:
            from_index = msg_obj.from_message_ids.index(event.message.id)
            to_message_id = msg_obj.to_message_ids[from_index]
        except (ValueError, IndexError):
            continue

        if to_chat_id and to_message_id:
            print(f"to_chat_id and to_message_id kam ekan. {to_chat_id} - {to_message_id}", event)
            await edit_single_message(event, to_chat_id, to_message_id)
