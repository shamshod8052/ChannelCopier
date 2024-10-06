from Admin.models import Channel, Message


async def check_channel(chat_id):
    try:
        return Channel.objects.get(chat_id=chat_id, goal=Channel.Goals.get)
    except Channel.DoesNotExist:
        return None


async def get_for_send_channels():
    channels = Channel.objects.filter(goal=Channel.Goals.send)
    return channels.all()


async def get_message_objs(chat_id, message_ids):
    try:
        messages = Message.objects.filter(from_chat_id=chat_id, from_message_ids__icontains=message_ids)
    except Message.DoesNotExist:
        return None
    else:
        return messages.all()
