import re
from typing import Optional

from telethon.extensions import html
from telethon.tl.types import (
    MessageEntityMention, MessageEntityUrl, MessageEntityEmail,
    MessageEntityTextUrl, MessageEntityMentionName, InputMessageEntityMentionName,
    MessageEntityPhone
)


class Cleaner:
    def __init__(self, text: str = '', entities=None, extra_text: str = ''):
        if entities is None:
            entities = []
        self.text = text
        self.entities = entities
        self.extra_text = extra_text

    async def clean_text(self):
        if not self.text:
            return self.text, self.entities
        cleaned_regex = await self.clean_ads_with_regex(self.text)
        cleaned_other = await self.clean_text_preserve_format(cleaned_regex)

        text = (f"<b>{cleaned_other}</b>"
                f"\n\n{self.extra_text}")
        cleaned_text, cleaned_entities = html.parse(text)

        return cleaned_text, cleaned_entities

    async def clean_text_preserve_format(self, text: Optional[str] = None):
        if text is None:
            text = self.text
        text = re.sub(r'( *\n *){3,}', '\n\n', text)
        text = re.sub(r'[ \t]{3,}', '  ', text)

        return text.strip()

    async def clean_ads_with_entities(self, text: Optional[str] = None, entities: Optional[list] = None):
        if text is None:
            text = self.text
        if entities is None:
            entities = self.entities
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

    async def clean_ads_with_regex(self, text: Optional[str] = None):
        if text is None:
            text = self.text

        PHONE_PATTERN_UZ = r'\+?998([- .])?(90|91|93|94|95|98|99|33|97|71)([- .])?(\d{3})([- .])?(\d{2})([- .])?(\d{2})'
        USERNAME_PATTERN = r'@\w+'
        URL_PATTERN = r'(?:http[s]?://|www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[^\s]*)?'
        removed_phone = re.sub(PHONE_PATTERN_UZ, '', text)
        removed_username = re.sub(USERNAME_PATTERN, '', removed_phone)
        removed_url = re.sub(URL_PATTERN, '', removed_username)

        return removed_url
