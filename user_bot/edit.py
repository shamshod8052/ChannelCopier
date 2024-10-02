from telethon.errors.rpcerrorlist import MessageNotModifiedError

from user_bot.loader import client
from user_bot.message import MyMessage
from user_bot.text_cleaner import TextCleaner


class EditedMessage(MyMessage):
    def __init__(self, event):
        super().__init__(event)
        self.to_chat_id = None
        self.to_message_id = None

    async def edit(self):
        message_obj = await self._get_message_obj(self.event.message.id)
        if not message_obj:
            return

        self.to_chat_id = int(message_obj.to_chat_id)
        from_index = message_obj.from_message_ids.index(self.event.message.id)
        self.to_message_id = message_obj.to_message_ids[from_index]

        if not (self.to_chat_id and self.to_message_id):
            return

        await self._edit_single_message()

    async def _edit_single_message(self):
        try:
            helper_msg = self.event.original_update.message
            text = await TextCleaner.clean_text(helper_msg.message, helper_msg.entities)
            helper_msg.message = text
            await client.edit_message(self.to_chat_id, message=self.to_message_id, text=text, file=helper_msg)
        except MessageNotModifiedError:
            pass
        except Exception as e:
            print(f"Error editing message: {e}")
