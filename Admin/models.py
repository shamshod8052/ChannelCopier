from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.IntegerField(unique=True, null=True, blank=True)
    status = models.BooleanField(default=False)
    about = models.TextField(null=True, blank=True)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.full_name or self.chat_id

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Channel(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.IntegerField(unique=True)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

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


class Message(models.Model):
    class EDITE(models.IntegerChoices):
        OTHER = 0, 'By other channel'
        ADMIN = 1, 'By admin'
        REAL = 2, 'Real message'

    class DELETE(models.IntegerChoices):
        OTHER = 0, 'By other channel'
        ADMIN = 1, 'By admin'
        AVAILABLE = 2, 'Available'

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    message_id = models.IntegerField()
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
    from_msg = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='from_united')
    to_msg = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='to_united')

    def __str__(self):
        return f"{self.from_msg.channel} -> {self.to_msg.channel}"

    class Meta:
        verbose_name = "CopyLink"
        verbose_name_plural = "CopyLinks"
