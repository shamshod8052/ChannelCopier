import datetime
import logging
from dataclasses import dataclass
from typing import Optional, List, Union

import pytz
from django.db import models
from django.db.models import Max
from telethon import TelegramClient
from telethon.tl.types import Message as TeleMessage
from tinymce.models import HTMLField

from UserBot.config import COPY_START_TIME, INTERVAL_SECONDS


class User(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    process_status = models.BooleanField(default=False)
    about = models.TextField(null=True, blank=True)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    @property
    def extra_text(self):
        texts = self.extra_texts.filter(status=True)
        if texts.exists():
            return texts.first().text
        return ''

    def __str__(self):
        return self.full_name or self.chat_id

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class ERROR:
    @dataclass
    class READY:
        message: Optional[str] = None
    @dataclass
    class TIME:
        time_diff: Optional[datetime.timedelta] = None
    @dataclass
    class TIME_INTERVAL:
        time_diff: Optional[datetime.timedelta] = None
    @dataclass
    class EQUAL_GROUPED_ID:
        message: Optional[str] = None


class Channel(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.BigIntegerField(unique=True)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    grouped_id: Optional[int] = None

    async def get_channel_last_message(self, client: TelegramClient) -> TeleMessage:
        last_message = None
        async for m in client.iter_messages(self.chat_id, limit=1):
            last_message = m

        return last_message

    async def get_free_messages_ids(self, client: TelegramClient) -> List[int]:
        last_msg_obj = await self.messages.get_last_obj()
        channel_last_msg = await self.get_channel_last_message(client)

        if not last_msg_obj:
            last_msg_id = channel_last_msg.id
        else:
            last_msg_id = last_msg_obj.message_id + 1

        return list(range(last_msg_id, channel_last_msg.id + 1))

    async def check_message(self, message: TeleMessage) -> Union[
        ERROR.READY, ERROR.TIME, ERROR.TIME_INTERVAL, ERROR.EQUAL_GROUPED_ID
    ]:
        time_diff = datetime.datetime.now(pytz.timezone('Asia/Tashkent')) - message.date
        if time_diff.seconds > COPY_START_TIME:
            return ERROR.TIME(time_diff)
        if time_diff.seconds <= INTERVAL_SECONDS:
            return ERROR.TIME_INTERVAL(time_diff)
        if message.grouped_id and message.grouped_id == self.grouped_id:
            return ERROR.EQUAL_GROUPED_ID()

        return ERROR.READY()

    async def get_free_messages_group(self, client: TelegramClient) -> List[TeleMessage]:
        """Kanaldagi yuborilmagan xabarlar ro'yxati. media_group uchun bitta message_id olinadi."""
        msgs_group = []
        is_continue, begin_message_id = False, None
        msg_ids = await self.get_free_messages_ids(client)
        messages = await client.get_messages(self.chat_id, ids=msg_ids)
        for message in messages:
            if not message:
                logging.info(f"Not message")
                continue
            if message.id == begin_message_id:
                is_continue = False
            if is_continue:
                logging.info(f"Continued: is_continue=True")
                continue
            error_type = await self.check_message(message)
            if isinstance(error_type, ERROR.TIME):
                logging.info(f"The message is too old.")
                last_messages = await client.get_messages(
                    self.chat_id,
                    limit=1,
                    offset_date=error_type.time_diff,
                    reverse=True
                )
                if last_messages:
                    begin_message_id = last_messages[0].id
                else:
                    break
                is_continue = True
                continue
            if isinstance(error_type, ERROR.TIME_INTERVAL):
                logging.info(f"Message time is less than interval")
                break
            if isinstance(error_type, ERROR.EQUAL_GROUPED_ID):
                logging.info(f"This media group member has already been added.")
                continue

            msgs_group.append(message)
            self.grouped_id = message.grouped_id

        return msgs_group[:-1]

    def __str__(self):
        return self.full_name or self.chat_id

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"


class Sender(models.Model):
    """Channel with new message"""
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='senders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders')

    def __str__(self):
        return f"Sender: {self.user.full_name} - {self.channel.full_name}"

    class Meta:
        verbose_name = "Sender"
        verbose_name_plural = "Senders"
        unique_together = ('channel', 'user')


class Getter(models.Model):
    """Channel to send new message"""
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='getters')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='getters')

    def __str__(self):
        return f"Getter: {self.user.full_name} - {self.channel.full_name}"

    class Meta:
        verbose_name = "Getter"
        verbose_name_plural = "Getters"
        unique_together = ('channel', 'user')


class MessageManager(models.Manager):
    async def get_last_obj(self) -> Optional['Message']:
        if self.exists():
            max_msg_id = self.aggregate(Max('message_id'))['message_id__max']
            return self.get(message_id=max_msg_id)
        else:
            return None


class Message(models.Model):
    class EDITE(models.IntegerChoices):
        OTHER = 0, 'By other channel'
        ADMIN = 1, 'By admin'
        REAL = 2, 'Real message'

    class DELETE(models.IntegerChoices):
        OTHER = 0, 'By other channel'
        ADMIN = 1, 'By admin'
        AVAILABLE = 2, 'Available'

    objects = MessageManager()

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    message_id = models.BigIntegerField()
    grouped_id = models.CharField(max_length=255, null=True, blank=True)
    edited_by = models.IntegerField(choices=EDITE.choices, default=EDITE.REAL)
    deleted_by = models.IntegerField(choices=DELETE.choices, default=DELETE.AVAILABLE)

    updated_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return f"{self.message_id} - {self.channel}"

    @property
    def get_message_id(self):
        return int(self.message_id)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        unique_together = ['channel', 'message_id']


class CopyLink(models.Model):
    from_msg = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='from_link')
    to_msg = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='to_link')

    def __str__(self):
        return f"{self.from_msg.channel} -> {self.to_msg.channel}"

    class Meta:
        verbose_name = "CopyLink"
        verbose_name_plural = "CopyLinks"
        unique_together = ['from_msg', 'to_msg']


class ExtraText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='extra_texts')
    text = HTMLField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "ExtraText"
        verbose_name_plural = "ExtraTexts"
