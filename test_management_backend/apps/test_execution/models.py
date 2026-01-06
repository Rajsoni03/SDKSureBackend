"""Models for managing test execution."""
from django.conf import settings
from django.db import models
from django.utils import timezone


class TestScenario(models.Model):
    """Scenario grouping multiple test cases."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    test_cases = models.ManyToManyField("test_cases.TestCase", related_name="scenarios", blank=True)
    labels = models.ManyToManyField("test_cases.Label", related_name="scenarios", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_scenarios"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_scenarios"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TestRun(models.Model):
    """Represents a single execution run that can contain multiple scenarios."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scenarios = models.ManyToManyField(TestScenario, related_name="test_runs", blank=True)
    labels = models.ManyToManyField("test_cases.Label", related_name="test_runs", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_test_runs"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_test_runs"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class TestResult(models.Model):
    """Result log entries for a test run."""

    STATUS_CHOICES = [
        ("INFO", "Info"),
        ("WARN", "Warn"),
        ("ERROR", "Error"),
    ]

    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name="results")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="INFO")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
