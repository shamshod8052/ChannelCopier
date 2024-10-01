from Admin.models import Message
from user_bot.loader import client
from user_bot.text_cleaner import TextCleaner


class EditedMessageHandler:
    """
    Handler class for processing and editing incoming messages.
    It retrieves the message from the database and updates the corresponding message in the destination chat.
    """

    def __init__(self, event):
        """
        Initialize with the incoming event and prepare placeholders for destination message details.

        :param event: The incoming message event from Telegram.
        """
        self.event = event
        self.to_chat_id = None  # Destination chat ID where the message needs to be edited
        self.to_message_id = None  # Destination message ID to be edited

    async def process_message(self):
        """
        Process the incoming message by retrieving the related message object from the database
        and attempting to edit the existing message in the destination chat.

        :return: None
        """
        message_obj = await self._get_message_obj()
        if not message_obj:
            # If the related message object doesn't exist in the database, stop the process
            return

        # Set the target chat ID and message ID
        self.to_chat_id = int(message_obj.to_chat_id)
        self.to_message_id = int(message_obj.to_message_id)

        if not (self.to_chat_id and self.to_message_id):
            # If either the target chat ID or message ID is missing, we stop the process
            return

        # Proceed to edit the message
        await self._edit_single_message()

    async def _get_message_obj(self):
        """
        Retrieve the message object from the database based on the event's chat ID and message ID.

        :return: Message object or None if the corresponding message isn't found.
        """
        try:
            # Fetch the message object using chat ID and message ID
            return Message.objects.get(from_chat_id=self.event.chat_id, from_message_id=self.event.message.id)
        except Message.DoesNotExist:
            # If the message is not found in the database, return None
            return None

    async def _edit_single_message(self):
        """
        Edit the target message in the destination chat by cleaning the text
        and updating the message with the new content.

        :return: None
        """
        try:
            # Get the incoming message's content
            msg = self.event.message

            # Clean the text (remove unnecessary characters, fix markdown, etc.)
            text = await TextCleaner.clean_text(msg.message, msg.entities)

            # Use the Telegram client to edit the message in the target chat with the cleaned text
            await client.edit_message(self.to_chat_id, message=self.to_message_id, text=text)
        except Exception as e:
            # Log any errors that occur during the editing process (can be extended with logging)
            print(f"Error editing message: {e}")
