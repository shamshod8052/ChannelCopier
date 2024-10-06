from Admin.models import Message
from user_bot.loader import client
from user_bot.message import check_channel, get_for_send_channels
from user_bot.text_cleaner import clean_text


async def get_media_posts_in_group(chat, original_post, max_amp=10) -> list:
    if original_post.grouped_id is None:
        return [original_post] if original_post.media is not None else []

    search_ids = [i for i in range(original_post.id - max_amp, original_post.id + max_amp + 1)]
    posts = await client.get_messages(chat, ids=search_ids)
    media = []
    for post in posts:
        if post is not None and post.grouped_id == original_post.grouped_id and post.media is not None:
            media.append(post)
    return media


async def send_album(send_chat_id, posts):
    caption = None
    for message in posts:
        if message.text:
            caption = await clean_text(message.text, message.entities)
            break

    to_msgs = await client.send_file(send_chat_id, file=posts, caption=caption, parse_mode='markdown')
    return posts, to_msgs


async def send_media_group(album):
    chat_id = album.messages[0].chat_id
    get_channel = await check_channel(chat_id)
    if not get_channel:
        return

    channels = await get_for_send_channels()
    if not channels:
        return
    print(album)
    for channel in channels:
        posts = await get_media_posts_in_group(chat_id, album.messages[0])
        from_msgs, to_msgs = await send_album(int(channel.chat_id), posts)

        if not from_msgs or not to_msgs:
            return

        from_message_ids = [m.id for m in from_msgs]
        to_message_ids = [m.id for m in to_msgs]
        Message.objects.get_or_create(
            from_chat_id=chat_id, from_message_ids=from_message_ids,
            to_chat_id=channel.chat_id, to_message_ids=to_message_ids
        )
