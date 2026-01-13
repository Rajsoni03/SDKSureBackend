from django.contrib import admin

from .models import DashboardMetric


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ("key", "refreshed_at")
    search_fields = ("key",)

