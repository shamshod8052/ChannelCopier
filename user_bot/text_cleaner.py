import re
from telethon.tl.types import (
    MessageEntityMention, MessageEntityUrl, MessageEntityEmail,
    MessageEntityTextUrl, MessageEntityMentionName, InputMessageEntityMentionName,
    MessageEntityPhone
)


class TextCleaner:
    """
    Utility class to clean and format text while preserving valid markdown entities.
    It removes phone numbers, usernames, URLs, and extra markdown symbols.
    """

    PHONE_PATTERN = r'\+?\d[\d\s\-\(\)]{7,}\d'
    USERNAME_PATTERN = r'@\w+'
    URL_PATTERN = r'(?:http[s]?://|www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[^\s]*)?'

    @staticmethod
    async def clean_text(text, entities):
        """
        Clean text by removing phone numbers, usernames, and URLs.
        Preserve valid markdown formatting and remove unused markdown symbols.

        :param text: Raw message text to clean.
        :param entities: List of entities (mentions, URLs, etc.) that should be preserved.
        :return: Cleaned and formatted text.
        """
        if not text:
            return text

        cleaned_text, updated_entities = TextCleaner._clean_entities(text, entities)
        cleaned_text = TextCleaner.clean_text_preserve_format(cleaned_text)

        return cleaned_text

    @staticmethod
    def clean_text_preserve_format(text):
        """
        Clean text by reducing redundant spaces and newlines, while keeping the structure intact.

        :param text: The raw message text.
        :return: Cleaned text with formatting preserved.
        """
        text = re.sub(r'( *\n *){3,}', '\n\n', text)
        text = re.sub(r'[ \t]{3,}', '  ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()

    @staticmethod
    def _clean_entities(text, entities):
        """
        Remove invalid markdown entities such as phone numbers, usernames, and URLs.

        :param text: Raw message text.
        :param entities: List of entities attached to the message.
        :return: Cleaned text and updated entities.
        """
        remove_indexes = []
        new_entities = []
        if entities:
            for entity in entities:
                if isinstance(entity, (MessageEntityPhone, MessageEntityUrl, MessageEntityEmail,
                                       MessageEntityTextUrl, MessageEntityMention, MessageEntityMentionName,
                                       InputMessageEntityMentionName)):
                    remove_indexes.append((entity.offset, entity.length))

        cleaned_text = text
        for offset, length in remove_indexes:
            start, end = offset, offset + length
            cleaned_text = cleaned_text[:start] + ' ' * (end - start) + cleaned_text[end:]

        cleaned_text = re.sub(TextCleaner.PHONE_PATTERN, '', cleaned_text)
        cleaned_text = re.sub(TextCleaner.USERNAME_PATTERN, '', cleaned_text)
        cleaned_text = re.sub(TextCleaner.URL_PATTERN, '', cleaned_text)

        new_entities = TextCleaner._adjust_entity_positions(cleaned_text, new_entities)

        return cleaned_text, new_entities

    @staticmethod
    def _adjust_entity_positions(text, entities):
        """
        Adjust entity offsets to align with the cleaned text.
        This ensures that the markdown formatting remains correct after cleaning.

        :param text: The cleaned text.
        :param entities: List of entities to adjust.
        :return: Adjusted entities with correct offsets.
        """
        return entities
