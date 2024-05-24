from django.contrib import admin
from main.models import AccessKey, KeyToken


class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ["user", "status", "expiry_date", "created_at"]
    search_fields = ["user", "status"]
    list_filter = ["status"]


class KeyTokenAdmin(admin.ModelAdmin):
    list_display = ["key", "user", "status", "created_at"]
    search_fields = ["key", "user"]
    list_filter = ["user"]


admin.site.register(AccessKey, AccessKeyAdmin)
admin.site.register(KeyToken, KeyTokenAdmin)
# Register your models here.
