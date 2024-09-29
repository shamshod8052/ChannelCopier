from django.db import models


class Channel(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.CharField(max_length=255)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"


class User(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    admins = models.ManyToManyField('User', blank=True, related_name='boss')
    channels = models.ManyToManyField(Channel, blank=True, related_name='users')
    channel_for_send = models.ForeignKey(Channel, null=True, blank=True, on_delete=models.SET_NULL, related_name='user')

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
