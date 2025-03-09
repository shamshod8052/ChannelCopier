from django.contrib import admin
from .models import User, Channel, Sender, Getter, Message, CopyLink, ExtraText


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'chat_id', 'process_status', 'update_at', 'created_at')
    list_filter = ('process_status',)
    search_fields = ('full_name', 'username', 'chat_id')
    readonly_fields = ('update_at', 'created_at')

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'chat_id', 'update_at', 'created_at')
    search_fields = ('full_name', 'username', 'chat_id')
    readonly_fields = ('update_at', 'created_at')

@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel')
    list_filter = ('user', 'channel')
    search_fields = ('user__full_name', 'channel__full_name')

@admin.register(Getter)
class GetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel')
    list_filter = ('user', 'channel')
    search_fields = ('user__full_name', 'channel__full_name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('channel', 'message_id', 'grouped_id', 'edited_by_display', 'deleted_by_display', 'created_at')
    list_filter = ('edited_by', 'deleted_by', 'channel')
    search_fields = ('message_id', 'grouped_id')
    readonly_fields = ('created_at', 'updated_at')

    def edited_by_display(self, obj):
        return obj.get_edited_by_display()
    edited_by_display.short_description = 'Edited By'

    def deleted_by_display(self, obj):
        return obj.get_deleted_by_display()
    deleted_by_display.short_description = 'Deleted By'

@admin.register(CopyLink)
class CopyLinkAdmin(admin.ModelAdmin):
    list_display = ('from_msg', 'to_msg')
    search_fields = (
        'from_msg__message_id',
        'to_msg__message_id',
        'from_msg__channel__full_name',
        'to_msg__channel__full_name'
    )

@admin.register(ExtraText)
class ExtraTextAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')
    search_fields = ('text',)
    list_filter = ('status',)
