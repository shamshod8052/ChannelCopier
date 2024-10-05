from django.db.models import Q
from Admin.models import Channel, User, Message
from user_bot.loader import logger


class MyMessage:
    """
    A helper class that provides methods to handle message-related tasks,
    such as retrieving channels, users, and messages from the database.
    """

    def __init__(self, event):
        """
        Initialize the MyMessage class with the event data.

        :param event: Incoming event containing message data.
        """
        self.event = event

    @staticmethod
    async def get_channel(chat_id):
        """
        Retrieve the Channel object by its chat ID.

        :param chat_id: The chat ID of the channel to retrieve.
        :return: Channel object if found, otherwise None.
        """
        try:
            return Channel.objects.get(chat_id=chat_id)
        except Channel.DoesNotExist:
            return None

    @staticmethod
    async def get_send_chat_id(channel):
        """
        Retrieve the send chat ID from the channel if the user is an admin or has a boss assigned.

        :param channel: The Channel object for which we want the send chat ID.
        :return: The send chat ID as an integer, or None if conditions are not met.
        """
        # Check if the channel has users and whether they are admin or have a boss.
        if not (channel.users.exists() and (channel.users.first().is_admin or channel.users.first().boss.exists())):
            logger.info(f"Not admin and not boss. chat_id: {channel}")
            return None

        # Filter for admin users who have a send channel assigned.
        admin_users = User.objects.filter(~Q(channel_for_send=None), is_admin=True)
        if not admin_users.exists():
            logger.info(f"Not channel for send. chat_id: {channel}")
            return None

        # Return the chat ID for the first valid admin user.
        return int(admin_users.first().channel_for_send.chat_id)

    async def get_message_obj(self, message_ids):
        """
        Retrieve the message object by matching the message ID with the event's chat ID.

        :param message_ids: List of message IDs to search for in the database.
        :return: Message object if found, otherwise None.
        """
        try:
            # Use a lookup for multiple message IDs in the `from_message_ids` field.
            return Message.objects.get(from_chat_id=self.event.chat_id, from_message_ids__contains=message_ids)
        except Message.DoesNotExist:
            logger.info(f"Not available message_obj. chat_id: {self.event.chat_id}, msg_id: {self.event.message.id}")
            return None
