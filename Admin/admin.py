from django.contrib import admin

from Admin.models import User, Channel, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'chat_id', 'is_admin', 'update_at', 'created_at')
    search_fields = ('full_name', 'username', 'chat_id')


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'chat_id', 'added_user', 'goal', 'update_at', 'created_at')
    search_fields = ('full_name', 'username', 'chat_id')
    list_filter = ('goal', 'update_at', 'created_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_chat_id', 'to_chat_id', 'update_at', 'created_at')
    search_fields = ('from_chat_id', 'to_chat_id', 'from_message_ids', 'to_message_ids')
