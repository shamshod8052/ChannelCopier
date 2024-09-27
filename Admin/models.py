from django.db import models


class Channel(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"


class User(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)
    channels = models.ManyToManyField(Channel)

    update_at = models.DateTimeField(verbose_name='Last activity', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
