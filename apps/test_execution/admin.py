from django.contrib import admin

from .models import TestResult, TestRun, TestScenario


@admin.register(TestScenario)
class TestScenarioAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "updated_by", "created_at", "updated_at")
    search_fields = ("name", "description")
    filter_horizontal = ("test_cases", "labels")


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "updated_by", "created_at", "updated_at")
    search_fields = ("name", "description")
    filter_horizontal = ("scenarios", "labels")


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("test_run", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("message",)
