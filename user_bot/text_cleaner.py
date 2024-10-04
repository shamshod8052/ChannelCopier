import re
from telethon.tl.types import (
    MessageEntityMention, MessageEntityUrl, MessageEntityEmail,
    MessageEntityTextUrl, MessageEntityMentionName, InputMessageEntityMentionName,
    MessageEntityPhone
)


class TextCleaner:
    """
    A utility class to clean text by removing advertisements, phone numbers, URLs, and mentions,
    while preserving the general formatting of the text.
    """

    # Define patterns for phone numbers, usernames, and URLs
    PHONE_PATTERN = r'\+?\d[\d\s\-\(\)]{7,}\d'
    USERNAME_PATTERN = r'@\w+'
    URL_PATTERN = r'(?:http[s]?://|www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[^\s]*)?'

    @staticmethod
    async def clean_text(text, entities=None):
        """
        Main method to clean text using both regex and entity-based methods.

        :param text: Raw input text to clean.
        :param entities: Optional list of message entities to preserve certain parts.
        :return: Cleaned text.
        """
        if not text:
            return text

        # Clean ads or unwanted parts from text using regex
        cleaned_text = TextCleaner._clean_ads_with_regex(text)

        # Optionally, clean text based on message entities
        cleaned_text, updated_entities = TextCleaner._clean_ads_with_entities(cleaned_text, entities)

        # Preserve formatting (limit excessive newlines or spaces)
        cleaned_text = TextCleaner.clean_text_preserve_format(cleaned_text)
        cleaned_text = f"**{cleaned_text}**"

        return cleaned_text

    @staticmethod
    def clean_text_preserve_format(text):
        """
        Preserves the formatting of the text by ensuring that no more than
        two consecutive newlines or spaces are present.

        :param text: The input text to clean up formatting.
        :return: Cleaned and formatted text.
        """
        text = re.sub(r'( *\n *){3,}', '\n\n', text)  # Limit consecutive newlines
        text = re.sub(r'[ \t]{3,}', '  ', text)       # Limit consecutive spaces or tabs
        return text.strip()

    @staticmethod
    def _clean_ads_with_entities(text, entities):
        """
        Cleans advertisements or unwanted parts from the text based on message entities.
        Removes mentions, URLs, and other entities as specified.

        :param text: The input text.
        :param entities: List of entities like mentions, URLs, emails, etc., to be cleaned.
        :return: Tuple of cleaned text and updated entities.
        """
        remove_indexes = []  # Track positions of entities to remove
        new_entities = []     # Updated entities list after cleaning
        ignore_indexes = []  # Need for ignore

        if entities:
            for entity in entities:
                # Identify the entities that we want to remove (mentions, URLs, etc.)
                if isinstance(entity, (MessageEntityPhone, MessageEntityUrl, MessageEntityEmail,
                                       MessageEntityTextUrl, MessageEntityMention, MessageEntityMentionName,
                                       InputMessageEntityMentionName)):
                    if isinstance(entity, MessageEntityPhone):
                        ignore_indexes.append((entity.offset, entity.length))
                    remove_indexes.append((entity.offset, entity.length))

        # Replace the text parts for the identified entities
        cleaned_text = text
        for offset, length in remove_indexes:
            if (offset, length) not in ignore_indexes:
                start, end = offset, offset + length
                # Replace the entity part with spaces to preserve alignment
                cleaned_text = cleaned_text[:start] + ' ' * (end - start) + cleaned_text[end:]

        return cleaned_text, new_entities

    @staticmethod
    def _clean_ads_with_regex(text):
        """
        Cleans advertisements or unwanted parts from the text using regular expressions.
        This method targets phone numbers, usernames, and URLs.

        :param text: The input text to clean.
        :return: Cleaned text without phone numbers, usernames, and URLs.
        """
        # Remove phone numbers, usernames, and URLs from the text
        cleaned_text = re.sub(TextCleaner.PHONE_PATTERN, '', text)
        cleaned_text = re.sub(TextCleaner.USERNAME_PATTERN, '', cleaned_text)
        cleaned_text = re.sub(TextCleaner.URL_PATTERN, '', cleaned_text)

        return cleaned_text
