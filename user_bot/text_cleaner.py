import re
from telethon.tl.types import (
    MessageEntityMention, MessageEntityUrl, MessageEntityEmail,
    MessageEntityTextUrl, MessageEntityMentionName, InputMessageEntityMentionName,
    MessageEntityPhone
)


async def clean_text(text, entities=None):
    if not text:
        return text

    cleaned_text = await clean_ads_with_regex(text)

    # cleaned_text, updated_entities = await clean_ads_with_entities(cleaned_text, entities)

    cleaned_text = await clean_text_preserve_format(cleaned_text)
    cleaned_text = f"{cleaned_text}"

    return cleaned_text


async def clean_text_preserve_format(text):
    text = re.sub(r'( *\n *){3,}', '\n\n', text)
    text = re.sub(r'[ \t]{3,}', '  ', text)
    return text.strip()


async def clean_ads_with_entities(text, entities):
    remove_indexes = []
    new_entities = []
    ignore_indexes = []

    if entities:
        for entity in entities:
            if isinstance(entity, (MessageEntityPhone, MessageEntityUrl, MessageEntityEmail,
                                   MessageEntityTextUrl, MessageEntityMention, MessageEntityMentionName,
                                   InputMessageEntityMentionName)):
                if isinstance(entity, MessageEntityPhone):
                    ignore_indexes.append((entity.offset, entity.length))
                remove_indexes.append((entity.offset, entity.length))

    cleaned_text = text
    for offset, length in remove_indexes:
        if (offset, length) not in ignore_indexes:
            start, end = offset, offset + length
            cleaned_text = cleaned_text[:start] + ' ' * (end - start) + cleaned_text[end:]

    return cleaned_text, new_entities


async def clean_ads_with_regex(text):
    PHONE_PATTERN = r'\+?\d[\d\s\-\(\)]{7,}\d'
    USERNAME_PATTERN = r'@\w+'
    URL_PATTERN = r'(?:http[s]?://|www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[^\s]*)?'

    cleaned_text = re.sub(PHONE_PATTERN, '', text)
    cleaned_text = re.sub(USERNAME_PATTERN, '', cleaned_text)
    cleaned_text = re.sub(URL_PATTERN, '', cleaned_text)

    return cleaned_text
