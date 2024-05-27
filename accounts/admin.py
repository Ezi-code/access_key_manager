from django.contrib import admin
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    search_fields = ["username", "email"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    ordering = ["is_superuser"]


admin.site.register(User, UserAdmin)
