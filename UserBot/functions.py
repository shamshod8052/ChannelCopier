import logging
import traceback

from Admin.models import Message, CopyLink, Channel


async def add_messages_for_base(from_chat_id, to_chat_id, from_msgs: list, to_msgs: list):
    if not from_msgs or not to_msgs:
        return

    for from_msg, to_msg in zip(from_msgs, to_msgs):
        try:
            from_msg_obj, cr = Message.objects.get_or_create(
                channel=Channel.objects.get(chat_id=from_chat_id),
                message_id=from_msg.id,
                grouped_id=from_msg.grouped_id
            )
            to_msg_obj, cr = Message.objects.get_or_create(
                channel=Channel.objects.get(chat_id=to_chat_id),
                message_id=to_msg.id,
                grouped_id=to_msg.grouped_id
            )
            CopyLink.objects.create(from_msg=from_msg_obj, to_msg=to_msg_obj)
        except:
            traceback.print_exc()
    logging.info("Message info added for base")
