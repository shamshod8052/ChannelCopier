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
    print(posts[0].id, "caption get success", caption)
    media = []
    force_document = False
    for group_message in posts:
        if group_message.photo:
            media.append(group_message.photo)
        elif group_message.video:
            media.append(group_message.video)
        elif group_message.document:
            media.append(group_message.document)
            force_document = True
    to_msgs = await client.send_file(send_chat_id, media, caption=caption, force_document=force_document)
    return posts, to_msgs


async def send_media_group(album):
    chat_id = album.messages[0].chat_id
    if not chat_id:
        print(album.messages[0].id, "chat_id is None", album)
    get_channel = await check_channel(chat_id)
    print(get_channel)
    if not get_channel:
        print(album.messages[0].id, "Channel not my list", album)
        return

    channels = await get_for_send_channels()
    if not channels:
        print(album.messages[0].id, "Not send channels", album)
        return
    for channel in channels:
        posts = await get_media_posts_in_group(chat_id, album.messages[0])
        if not posts:
            print(album.messages[0].id, "Don't get posts", album)
        from_msgs, to_msgs = await send_album(int(channel.chat_id), posts)
        if to_msgs:
            print(album.messages[0].id, "✅ Message sent successfully", album)
        else:
            print(album.messages[0].id, "❌ Posts not sent", album)
        if not from_msgs or not to_msgs:
            return

        from_message_ids = [m.id for m in from_msgs]
        to_message_ids = [m.id for m in to_msgs]
        Message.objects.get_or_create(
            from_chat_id=chat_id, from_message_ids=from_message_ids,
            to_chat_id=channel.chat_id, to_message_ids=to_message_ids
        )
