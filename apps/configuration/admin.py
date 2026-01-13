from django.contrib import admin

from .models import SystemConfiguration


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ("key", "updated_at")
    search_fields = ("key",)

