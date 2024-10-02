import asyncio

from telethon.errors.rpcerrorlist import MessageNotModifiedError
from user_bot.loader import client
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner


class EditedMessage(MyMessage):
    """
    Class to handle editing of already sent messages.
    It retrieves the message pair from the database and edits the content on the target channel.
    """

    def __init__(self, event):
        super().__init__(event)
        self.to_chat_id = None
        self.to_message_id = None

    async def edit(self):
        """
        Main method to edit the message. It first retrieves the corresponding
        message IDs and then sends the edited message.
        """
        # Retrieve the corresponding message object from the database
        message_obj = await self._get_message_obj(self.event.message.id)
        if not message_obj:
            return

        self.to_chat_id = int(message_obj.to_chat_id)

        # Get the index of the edited message to find its corresponding target message ID
        try:
            from_index = message_obj.from_message_ids.index(self.event.message.id)
            self.to_message_id = message_obj.to_message_ids[from_index]
        except (ValueError, IndexError):
            return

        # Edit the message if valid chat and message IDs are present
        if self.to_chat_id and self.to_message_id:
            await asyncio.sleep(7)
            await self._edit_single_message()

    async def _edit_single_message(self):
        """
        Sends an edit request to modify the message content. Cleans the text before sending.
        Handles potential errors during the editing process.
        """
        try:
            helper_msg = self.event.original_update.message

            # Clean the message text
            text = await TextCleaner.clean_text(helper_msg.message, helper_msg.entities)
            helper_msg.message = text

            # Send the edit request to the target chat
            await client.edit_message(
                self.to_chat_id,
                message=self.to_message_id,
                text=text,
                file=helper_msg
            )
        except MessageNotModifiedError:
            # Message content was not modified, no need to update
            pass
        except Exception as e:
            # Log or print the error message (replace with proper logging in production)
            print(f"Error editing message: {e}")
