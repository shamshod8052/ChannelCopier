from user_bot.loader import client
from user_bot.message import MyMessage


class DeleteMessage(MyMessage):
    def __init__(self, event):
        super().__init__(event)

        self.to_chat_id = None
        self.to_message_ids = []

    async def delete(self):
        message_obj = await self._get_message_obj(self.event.deleted_ids)
        if not message_obj:
            return

        self.to_chat_id = int(message_obj.to_chat_id)
        for from_id in self.event.deleted_ids:
            try:
                from_index = message_obj.from_message_ids.index(from_id)
            except ValueError:
                continue
            del message_obj.from_message_ids[from_index]
            self.to_message_ids.append(message_obj.to_message_ids.pop(from_index))
        message_obj.save()

        if not (self.to_chat_id and self.to_message_ids):
            return

        await self._delete_single_message()

    async def _delete_single_message(self):
        try:
            await client.delete_messages(self.to_chat_id, self.to_message_ids)
        except Exception as e:
            print(f"Error deleting message: {e}")
