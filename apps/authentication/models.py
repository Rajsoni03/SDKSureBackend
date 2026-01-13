"""Custom user model and related entities."""
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUserManager(UserManager):
    """Custom manager that uses email as username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "SUPER_ADMIN")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Extended user model with roles and board assignments."""

    ROLE_CHOICES = [
        ("SUPER_ADMIN", "Super Administrator"),
        ("ADMIN", "Administrator"),
        ("NORMAL_USER", "Normal User"),
    ]

    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="NORMAL_USER", db_index=True)
    assigned_boards = models.ManyToManyField(
        "boards.Board",
        related_name="assigned_users",
        blank=True,
        through="UserBoardAssignment",
        through_fields=("user", "board"),
    )

    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_count = models.IntegerField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.role == "SUPER_ADMIN"

    @property
    def is_admin(self):
        return self.role in ["SUPER_ADMIN", "ADMIN"]

    def has_board_access(self, board):
        if self.is_admin:
            return True
        return self.assigned_boards.filter(id=board.id).exists()


class UserBoardAssignment(models.Model):
    """Through model for user-board mapping with metadata."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey("boards.Board", on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assignments_made"
    )

    class Meta:
        unique_together = ("user", "board")
        ordering = ["-assigned_at"]
