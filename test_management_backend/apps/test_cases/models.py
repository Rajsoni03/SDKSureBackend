"""Test case related models."""
from django.conf import settings
from django.db import models


class TestType(models.Model):
    """Category for a test case."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Label(models.Model):
    """Label for grouping test cases."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TestCase(models.Model):
    """Reusable test case definition."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    test_type = models.ForeignKey(TestType, on_delete=models.SET_NULL, null=True, related_name="test_cases")
    tags = models.ManyToManyField(Label, related_name="test_cases", blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_test_cases"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        unique_together = ("title", "test_type")

    def __str__(self):
        return self.title
