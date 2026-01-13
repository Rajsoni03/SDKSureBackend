from django.db import models

from apps.boards.models import Board, TestPC


class TestRequest(models.Model):
    """Queued test execution request."""

    STATUS_CHOICES = [
        ("QUEUED", "QUEUED"),
        ("RUNNING", "RUNNING"),
        ("DONE", "DONE"),
        ("FAILED", "FAILED"),
    ]

    # identification / targeting
    platform = models.CharField(max_length=50, help_text="Target platform (matches Board.platform)")

    # execution targets
    executed_on_board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True)
    executed_on_pc = models.ForeignKey(TestPC, on_delete=models.SET_NULL, null=True, blank=True)

    # priority and requirements
    priority = models.IntegerField(default=0, help_text="Higher values are scheduled first")
    required_capabilities = models.CharField(max_length=255, blank=True, help_text="Comma-separated capability names")

    # lifecycle status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="QUEUED")

    # timing
    timeout = models.IntegerField(default=600, help_text="Timeout in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-priority", "created_at")
        verbose_name_plural = "TestRequests"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["platform"]),
            models.Index(fields=["priority"]),
        ]

    def __str__(self):
        return f"Request {self.id} - {self.platform} - {self.status}"
