"""Dashboard aggregation models."""
from django.db import models


class DashboardMetric(models.Model):
    """Cached metric for dashboard display."""

    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField(default=dict)
    refreshed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return self.key

