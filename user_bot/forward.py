from telethon.errors import MessageEmptyError

from Admin.models import Message
from user_bot.loader import client
from user_bot.message import get_channel, get_send_chat_id
from user_bot.text_cleaner import clean_text


async def forward_single_message(event, send_chat_id):
    helper_msg = event.message
    helper_msg.message = await clean_text(helper_msg.message, helper_msg.entities)
    helper_msg.entities = []

    try:
        msg = await client.send_message(send_chat_id, message=helper_msg, parse_mode='markdown')
        return [event.message], [msg]
    except MessageEmptyError:
        return [], []


async def forward(event):
    chat_id = event.chat_id
    channel = await get_channel(chat_id)
    if not channel:
        return
    send_chat_id = await get_send_chat_id(channel)
    if not send_chat_id:
        return
    print(event)
    from_msgs, to_msgs = await forward_single_message(event, send_chat_id)

    if not from_msgs or not to_msgs:
        return

    from_message_ids = [m.id for m in from_msgs]
    to_message_ids = [m.id for m in to_msgs]
    Message.objects.get_or_create(
        from_chat_id=chat_id, from_message_ids=from_message_ids,
        to_chat_id=send_chat_id, to_message_ids=to_message_ids
    )
