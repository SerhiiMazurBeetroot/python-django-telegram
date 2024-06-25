from django.contrib import admin
from .models import User
from .models import History


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "first_name",
        "last_name",
        "username",
        "date_created",
    )
    search_fields = ("telegram_id", "username")


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "action",
        "message_text",
        "date_created",
    )
    search_fields = ("telegram_id", "action")
