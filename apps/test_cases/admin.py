from django.contrib import admin

from .models import Label, TestCase, TestType


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("title", "test_type", "is_active", "created_at")
    search_fields = ("title", "description")
    list_filter = ("is_active", "test_type")


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
