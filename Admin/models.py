from django.db import models


class Chat(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.CharField(max_length=255)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.full_name or self.chat_id

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class User(Chat):
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Channel(Chat):
    class Goals(models.IntegerChoices):
        send = 1, 'For send'
        get = 2, 'For get'
    added_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='channels', null=True, blank=True)
    goal = models.IntegerField(choices=Goals.choices, null=True, blank=True)

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channel"


class Message(models.Model):
    from_chat_id = models.CharField(max_length=255)
    from_message_ids = models.JSONField(default=list, null=True, blank=True)
    to_chat_id = models.CharField(max_length=255)
    to_message_ids = models.JSONField(default=list, null=True, blank=True)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.from_chat_id

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
