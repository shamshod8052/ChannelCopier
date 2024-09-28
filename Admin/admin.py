from django.contrib import admin

from Admin.models import User, Channel


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'chat_id', 'is_admin', 'update_at', 'created_at')


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'chat_id', 'update_at', 'created_at')
