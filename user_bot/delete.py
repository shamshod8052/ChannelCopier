from user_bot.loader import client
from user_bot.message import MyMessage
import logging


class DeleteMessage(MyMessage):
    """
    Class to handle deleting messages based on incoming deleted message events.
    It retrieves the corresponding messages and deletes them from the target chat.
    """

    def __init__(self, event):
        super().__init__(event)
        self.to_chat_id = None
        self.to_message_ids = []

    async def delete(self):
        """
        Main method to delete messages. It fetches the message object based on deleted IDs,
        removes the relevant messages from the database, and proceeds to delete them in the target chat.
        """
        # Retrieve the message object based on the deleted message IDs
        message_obj = await self._get_message_obj(self.event.deleted_ids)
        if not message_obj:
            return

        self.to_chat_id = int(message_obj.to_chat_id)

        # Match deleted message IDs and adjust the message object accordingly
        for from_id in self.event.deleted_ids:
            try:
                # Find the corresponding message ID and remove it from the database
                from_index = message_obj.from_message_ids.index(from_id)
                del message_obj.from_message_ids[from_index]
                self.to_message_ids.append(message_obj.to_message_ids.pop(from_index))
            except ValueError:
                # If the message ID is not found, skip it
                continue

        # Save the updated message object after removal
        message_obj.save()

        # If valid chat ID and message IDs are present, proceed with the deletion
        if self.to_chat_id and self.to_message_ids:
            await self._delete_single_message()

    async def _delete_single_message(self):
        """
        Sends the delete request to remove the messages from the target chat.
        Handles any errors that may occur during the deletion process.
        """
        try:
            await client.delete_messages(self.to_chat_id, self.to_message_ids)
        except Exception as e:
            # Log any errors encountered during message deletion
            logging.error(f"Error deleting message in chat {self.to_chat_id}: {e}")
