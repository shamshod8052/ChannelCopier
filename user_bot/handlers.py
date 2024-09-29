import asyncio
import re

from django.db.models import Q
from telethon import events
from telethon.events.newmessage import NewMessage

from Admin.models import Channel, User
from user_bot.loader import client

media_groups = dict()


def clean_text(text):
    if not text:
        return text

    phone_pattern = r'\+?\d[\d\s\-\(\)]{7,}\d'
    username_pattern = r'@\w+'
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    text = re.sub(phone_pattern, '', text)

    text = re.sub(username_pattern, '', text)

    text = re.sub(url_pattern, '', text)

    return text.strip()


@client.on(events.NewMessage)
async def echo_(event: NewMessage.Event):
    try:
        channel = Channel.objects.get(chat_id=event.chat_id)
    except Channel.DoesNotExist:
        return

    if not (channel.users.exists() and (channel.users.first().is_admin or channel.users.first().boss.exists())):
        return
    send_for_users = User.objects.filter(~Q(channel_for_send=None), is_admin=True)
    if not send_for_users.exists():
        return
    channel_for_send = send_for_users.first().channel_for_send
    send_chat_id = int(channel_for_send.chat_id)

    if event.message.grouped_id:  # This is media group
        if not media_groups.get(event.message.grouped_id):
            media_groups[event.message.grouped_id] = dict()
            media_groups[event.message.grouped_id]['messages'] = []
            media_groups[event.message.grouped_id]['message_ids'] = []
            if event.message.message:
                media_groups[event.message.grouped_id]['text'] = event.message.message
        media_groups[event.message.grouped_id]['messages'].append(event.message)
        media_groups[event.message.grouped_id]['message_ids'].append(event.message.id)
        
        await asyncio.sleep(1)
        if event.message.id == media_groups[event.message.grouped_id].get('message_ids')[0]:
            medias = media_groups[event.message.grouped_id].get('messages')
            text = media_groups[event.message.grouped_id].get('text')
            caption = clean_text(text)
            await client.send_file(send_chat_id, file=medias, caption=caption)
        else:
            return
    else:
        msg = event.message
        msg.message = clean_text(msg.message)
        await client.send_message(send_chat_id, message=msg)
        return
