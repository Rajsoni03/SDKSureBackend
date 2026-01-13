from django.contrib import admin

from .models import TestRequest


@admin.register(TestRequest)
class TestRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "platform", "status", "priority", "executed_on_board", "created_at", "started_at", "completed_at")
    list_filter = ("status", "platform")
    search_fields = ("id", "platform", "executed_on_board__name")
    ordering = ("-priority", "-created_at")
