# Django Backend - In-Depth Implementation Plan

## Overview

Complete specification for building a production-grade Django backend for the test case management system with UART communication, real-time updates, and REST API.

---

## Backend Technology Stack

### Core Framework
- **Django 4.2 LTS** or **5.0+** (Latest stable)
- **Django REST Framework (DRF)** 3.14+
- **Django Channels** 4.0+ (WebSocket/ASGI)
- **Daphne** 4.0+ (ASGI server)

### Database & Caching
- **PostgreSQL 15+** (Primary database, ACID compliance)
- **Redis 7+** (Cache layer, message broker, session store)
- **pgBouncer** (Connection pooling for PostgreSQL)

### Asynchronous & Background Tasks
- **Celery 5.3+** (Distributed task queue)
- **Celery Beat** (Periodic task scheduling)
- **Redis** as broker (already in stack)

### Real-Time Communication
- **Pusher Python SDK 3.3+** (Real-time events)
- **django-rest-framework-simplejwt** (JWT authentication)
- **channels-redis** 4.0+ (Channel layer for Channels)

### Hardware Communication
- **pySerial 3.5+** (UART/Serial communication)
- **pyusb** (Optional: USB device detection)

### Utilities & Extensions
- **python-dotenv** (Environment variable management)
- **pydantic** 2.0+ (Data validation)
- **Pillow** (Image handling)
- **django-cors-headers** (CORS support)
- **django-filter** (Advanced filtering)
- **django-extensions** (Management commands)
- **whitenoise** (Static file serving)

### Testing & Quality
- **pytest** 7.4+
- **pytest-django** 4.5+
- **pytest-cov** (Coverage reporting)
- **factory-boy** 3.3+ (Test fixtures)
- **faker** (Fake data generation)
- **responses** (HTTP mocking)
- **black** (Code formatting)
- **flake8** (Linting)
- **isort** (Import sorting)
- **mypy** (Type checking)

### Monitoring & Logging
- **Sentry** (Error tracking)
- **python-json-logger** (JSON logging)
- **django-debug-toolbar** (Development debugging)

---

## Project Structure (Detailed)

```
test_management_backend/
│
├── config/                          # Django configuration
│   ├── __init__.py
│   ├── settings.py                  # Main settings (imports from settings/)
│   ├── urls.py                      # Root URL configuration
│   ├── asgi.py                      # ASGI configuration (Channels)
│   ├── wsgi.py                      # WSGI configuration (Gunicorn)
│   └── settings/
│       ├── __init__.py
│       ├── base.py                  # Base settings (all environments)
│       ├── development.py           # Development-specific
│       ├── production.py            # Production-specific
│       └── testing.py               # Testing-specific
│
├── apps/
│
│   ├── authentication/              # User authentication & authorization
│   │   ├── __init__.py
│   │   ├── admin.py                 # Django admin customization
│   │   ├── apps.py
│   │   ├── models.py                # Custom User model, Profile
│   │   ├── views.py                 # Login, logout, token refresh
│   │   ├── viewsets.py              # DRF ViewSets for users
│   │   ├── serializers.py           # User serializers
│   │   ├── permissions.py           # Role-based permission classes
│   │   ├── authentication.py        # Custom auth backends
│   │   ├── urls.py                  # Auth URLs
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   ├── test_permissions.py
│   │   │   └── conftest.py
│   │   └── migrations/
│   │
│   ├── boards/                      # Hardware board management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                # Board, BoardCapability, BoardLog
│   │   ├── viewsets.py              # Board, Capability ViewSets
│   │   ├── serializers.py
│   │   ├── filters.py               # Custom filters
│   │   ├── urls.py
│   │   ├── signals.py               # Model signals
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_viewsets.py
│   │   │   ├── test_filters.py
│   │   │   └── conftest.py
│   │   ├── migrations/
│   │   └── management/
│   │       ├── __init__.py
│   │       └── commands/
│   │           ├── __init__.py
│   │           ├── monitor_boards.py
│   │           └── sync_board_status.py
│   │
│   ├── test_cases/                  # Test case management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                # TestCase, TestType, Tag
│   │   ├── viewsets.py
│   │   ├── serializers.py
│   │   ├── validators.py            # Custom validators
│   │   ├── urls.py
│   │   ├── signals.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_viewsets.py
│   │   │   └── conftest.py
│   │   └── migrations/
│   │
│   ├── test_execution/              # Core test execution engine
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                # TestRun, TestResult
│   │   ├── viewsets.py              # TestRun ViewSet
│   │   ├── serializers.py
│   │   ├── filters.py
│   │   ├── permissions.py
│   │   ├── urls.py
│   │   ├── signals.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_viewsets.py
│   │   │   ├── test_execution.py
│   │   │   └── conftest.py
│   │   ├── migrations/
│   │   ├── tasks.py                 # Celery tasks
│   │   ├── execution/               # Execution sub-package
│   │   │   ├── __init__.py
│   │   │   ├── executor.py          # Core test executor
│   │   │   ├── state_machine.py     # TestRun state management
│   │   │   ├── uart_manager.py      # UART connection pool
│   │   │   ├── process_manager.py   # OS process management
│   │   │   ├── output_handler.py    # Output capture & streaming
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_executor.py
│   │   │       ├── test_uart.py
│   │   │       └── test_state_machine.py
│   │   └── uart/                    # UART communication sub-package
│   │       ├── __init__.py
│   │       ├── handler.py           # Main UART handler
│   │       ├── protocol.py          # Protocol definitions
│   │       ├── parser.py            # Message parsing
│   │       ├── checksums.py         # Checksum utilities
│   │       ├── exceptions.py        # Custom exceptions
│   │       └── tests/
│   │           ├── __init__.py
│   │           ├── test_handler.py
│   │           ├── test_parser.py
│   │           └── test_checksums.py
│   │
│   ├── realtime/                    # Real-time communication
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── consumers.py             # WebSocket consumers
│   │   ├── routing.py               # WebSocket URL routing
│   │   ├── events.py                # Event definitions & payloads
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── pusher.py            # Pusher event publishing
│   │   │   ├── websocket.py         # WebSocket message handling
│   │   │   └── channel_layer.py     # Channel layer utilities
│   │   ├── serializers.py           # Event serializers
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_consumers.py
│   │   │   ├── test_pusher.py
│   │   │   └── conftest.py
│   │   └── migrations/
│   │
│   ├── dashboard/                   # Analytics & monitoring
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                # Cached statistics
│   │   ├── viewsets.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── queries.py               # Database queries for analytics
│   │   ├── aggregations.py          # Data aggregation logic
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_queries.py
│   │   │   ├── test_viewsets.py
│   │   │   └── conftest.py
│   │   └── migrations/
│   │
│   ├── configuration/               # System configuration
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                # SystemConfiguration
│   │   ├── viewsets.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── defaults.py              # Default configuration values
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── conftest.py
│   │   └── migrations/
│   │
│   └── core/                        # Shared utilities
│       ├── __init__.py
│       ├── exceptions.py            # Custom exceptions
│       ├── logging.py               # Logging configuration
│       ├── utils.py                 # Utility functions
│       ├── validators.py            # Reusable validators
│       ├── decorators.py            # Custom decorators
│       ├── pagination.py            # Custom pagination classes
│       ├── filters.py               # Shared filter classes
│       ├── mixins.py                # ViewSet mixins
│       ├── constants.py             # App-wide constants
│       └── tests/
│           ├── __init__.py
│           └── test_utils.py
│
├── tests/                           # Integration & E2E tests
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration & fixtures
│   ├── factories.py                 # Test data factories
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_api_flow.py         # Full API workflow tests
│   │   ├── test_uart_flow.py        # UART communication flow
│   │   ├── test_realtime_flow.py    # Real-time updates flow
│   │   └── test_execution_flow.py   # Full test execution flow
│   └── e2e/
│       ├── __init__.py
│       ├── test_user_journey.py
│       ├── test_board_lifecycle.py
│       └── test_test_execution.py
│
├── docker/
│   ├── Dockerfile                   # Production Docker image
│   ├── Dockerfile.dev               # Development Docker image
│   ├── entrypoint.sh                # Docker entrypoint script
│   ├── nginx.conf                   # Nginx configuration
│   └── supervisord.conf             # Supervisord configuration
│
├── requirements/
│   ├── base.txt                     # Base dependencies
│   ├── development.txt              # Development additions
│   ├── production.txt               # Production additions
│   └── testing.txt                  # Testing additions
│
├── scripts/
│   ├── manage_db.sh                 # Database management
│   ├── deploy.sh                    # Deployment script
│   ├── migrate.sh                   # Migration helper
│   └── seed_data.sh                 # Seed database
│
├── docs/
│   ├── API.md                       # API documentation
│   ├── UART_PROTOCOL.md             # UART protocol spec
│   ├── ARCHITECTURE.md              # Architecture decisions
│   ├── SETUP.md                     # Setup instructions
│   ├── DEPLOYMENT.md                # Deployment guide
│   └── DEVELOPMENT.md               # Development workflow
│
├── .env.example                     # Example environment variables
├── .env.production                  # Production environment (not in git)
├── .gitignore                       # Git ignore rules
├── manage.py                        # Django management script
├── docker-compose.yml               # Local development compose
├── docker-compose.prod.yml          # Production compose
├── pytest.ini                       # Pytest configuration
├── .flake8                          # Flake8 configuration
├── .isort.cfg                       # isort configuration
├── pyproject.toml                   # Black & general config
└── README.md                        # Backend README
```

---

## Models Detailed Implementation

### User Model with Custom Authentication

```python
# apps/authentication/models.py

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.validators import MinLengthValidator

class CustomUserManager(UserManager):
    """Custom user manager with email as unique identifier"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create regular user"""
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'SUPER_ADMIN')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Extended user model with roles and board assignments"""
    
    ROLE_CHOICES = [
        ('SUPER_ADMIN', 'Super Administrator'),
        ('ADMIN', 'Administrator'),
        ('NORMAL_USER', 'Normal User'),
    ]
    
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='NORMAL_USER',
        db_index=True
    )
    
    assigned_boards = models.ManyToManyField(
        'boards.Board',
        related_name='assigned_users',
        blank=True,
        through='UserBoardAssignment'
    )
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For tracking login activity
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @property
    def is_super_admin(self):
        return self.role == 'SUPER_ADMIN'
    
    @property
    def is_admin(self):
        return self.role in ['SUPER_ADMIN', 'ADMIN']
    
    def has_board_access(self, board):
        """Check if user has access to specific board"""
        if self.is_admin:
            return True
        return self.assigned_boards.filter(id=board.id).exists()


class UserBoardAssignment(models.Model):
    """Through model for User-Board relationship with metadata"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignments_made'
    )
    
    class Meta:
        unique_together = ('user', 'board')
        ordering = ['-assigned_at']
```

### Board Model with UART Configuration

```python
# apps/boards/models.py

from django.db import models
from django.utils import timezone
from apps.core.validators import validate_uart_port

class Board(models.Model):
    """Hardware board (EVM) model"""
    
    STATUS_CHOICES = [
        ('CONNECTED', 'Connected'),
        ('DISCONNECTED', 'Disconnected'),
        ('OFFLINE', 'Offline'),
        ('ERROR', 'Error'),
    ]
    
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        validators=[MinLengthValidator(3)]
    )
    serial_number = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Unique identifier for hardware board"
    )
    description = models.TextField(blank=True)
    
    # UART Configuration
    uart_port = models.CharField(
        max_length=50,
        validators=[validate_uart_port],
        help_text="Serial port path (e.g., /dev/ttyUSB0, COM3)"
    )
    baud_rate = models.IntegerField(
        default=115200,
        choices=[
            (9600, '9600'),
            (19200, '19200'),
            (38400, '38400'),
            (57600, '57600'),
            (115200, '115200'),
            (230400, '230400'),
        ]
    )
    data_bits = models.IntegerField(default=8, choices=[(7, '7'), (8, '8')])
    stop_bits = models.IntegerField(default=1, choices=[(1, '1'), (2, '2')])
    parity = models.CharField(
        max_length=1,
        default='N',
        choices=[('N', 'None'), ('E', 'Even'), ('O', 'Odd')]
    )
    flow_control = models.BooleanField(default=False)
    
    # Status & Metadata
    connection_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DISCONNECTED',
        db_index=True
    )
    location = models.CharField(max_length=255, blank=True)
    firmware_version = models.CharField(max_length=50, blank=True)
    hardware_revision = models.CharField(max_length=50, blank=True)
    
    # Lifecycle
    is_active = models.BooleanField(default=True, db_index=True)
    is_locked = models.BooleanField(
        default=False,
        help_text="Lock board to prevent test execution"
    )
    
    # Relationships
    current_test_run = models.ForeignKey(
        'test_execution.TestRun',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.PROTECT,
        related_name='created_boards'
    )
    
    # Timestamps & Monitoring
    last_heartbeat = models.DateTimeField(null=True, blank=True, db_index=True)
    last_error = models.TextField(blank=True)
    last_error_time = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['connection_status', 'is_active']),
            models.Index(fields=['serial_number']),
            models.Index(fields=['is_locked']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.serial_number})"
    
    @property
    def is_online(self) -> bool:
        """Check if board is online based on heartbeat"""
        if not self.last_heartbeat:
            return False
        
        time_since_heartbeat = timezone.now() - self.last_heartbeat
        heartbeat_timeout = 60  # seconds
        return time_since_heartbeat.total_seconds() < heartbeat_timeout
    
    def update_heartbeat(self, status: str = 'CONNECTED'):
        """Update heartbeat and status"""
        self.last_heartbeat = timezone.now()
        
        if self.is_online:
            self.connection_status = status
        else:
            self.connection_status = 'OFFLINE'
        
        self.save(update_fields=['last_heartbeat', 'connection_status'])
        
        # Publish real-time update
        from apps.realtime.handlers.pusher import PusherHandler
        PusherHandler().publish_board_status(self)
    
    def log_error(self, error_message: str):
        """Log error and update board status"""
        self.last_error = error_message
        self.last_error_time = timezone.now()
        self.connection_status = 'ERROR'
        self.save(update_fields=['last_error', 'last_error_time', 'connection_status'])
    
    def can_execute_test(self) -> tuple[bool, str]:
        """Check if board can execute tests"""
        if not self.is_active:
            return False, "Board is not active"
        
        if self.is_locked:
            return False, "Board is locked"
        
        if not self.is_online:
            return False, "Board is offline"
        
        if self.current_test_run and self.current_test_run.is_running:
            return False, "Board is already executing a test"
        
        return True, "Ready"


class BoardCapability(models.Model):
    """Board capabilities/features"""
    
    CAPABILITY_CHOICES = [
        ('CMD', 'Command Execution'),
        ('CAMERA', 'Camera Testing'),
        ('DISPLAY', 'Display Output'),
        ('SENSOR', 'Sensor Reading'),
        ('GPIO', 'GPIO Control'),
        ('ADC', 'Analog to Digital'),
        ('NETWORK', 'Network'),
        ('STORAGE', 'Storage Test'),
        ('PERFORMANCE', 'Performance Metrics'),
        ('THERMAL', 'Thermal Management'),
        ('POWER', 'Power Management'),
        ('SECURITY', 'Security Features'),
    ]
    
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='capabilities'
    )
    name = models.CharField(
        max_length=50,
        choices=CAPABILITY_CHOICES,
        db_index=True
    )
    description = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=True, db_index=True)
    version = models.CharField(max_length=50, blank=True)
    
    # Support info
    supported_test_types = models.ManyToManyField(
        'test_cases.TestType',
        blank=True,
        related_name='+'
    )
    max_parallel_tests = models.IntegerField(default=1)
    estimated_time_per_test = models.IntegerField(
        default=0,
        help_text="Estimated time in seconds"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('board', 'name')
        ordering = ['name']
        indexes = [
            models.Index(fields=['board', 'is_enabled']),
        ]
    
    def __str__(self):
        return f"{self.board.name} - {self.get_name_display()}"


class BoardLog(models.Model):
    """Board activity audit log"""
    
    ACTION_CHOICES = [
        ('CONNECTED', 'Board Connected'),
        ('DISCONNECTED', 'Board Disconnected'),
        ('ERROR', 'Error Occurred'),
        ('TEST_STARTED', 'Test Started'),
        ('TEST_COMPLETED', 'Test Completed'),
        ('FIRMWARE_UPDATED', 'Firmware Updated'),
        ('CAPABILITY_ADDED', 'Capability Added'),
        ('CAPABILITY_REMOVED', 'Capability Removed'),
        ('STATUS_CHANGED', 'Status Changed'),
        ('LOCKED', 'Board Locked'),
        ('UNLOCKED', 'Board Unlocked'),
    ]
    
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        db_index=True
    )
    message = models.TextField()
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='board_logs_created'
    )
    details = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['board', 'action']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.board.name} - {self.get_action_display()}"
    
    @classmethod
    def log_action(cls, board, action: str, message: str, user=None, details=None):
        """Create a log entry"""
        return cls.objects.create(
            board=board,
            action=action,
            message=message,
            created_by=user,
            details=details or {}
        )
```

---

## API Endpoints - Complete Specification

### Authentication Endpoints

```python
# apps/authentication/urls.py

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = 'authentication'

router = DefaultRouter()
router.register('users', viewsets.UserViewSet, basename='user')

urlpatterns = [
    # Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('', include(router.urls)),
    path('profile/me/', viewsets.UserProfileView.as_view(), name='user_profile'),
    path('password/change/', viewsets.ChangePasswordView.as_view(), name='change_password'),
]
```

### Board Endpoints

```python
# apps/boards/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = 'boards'

router = DefaultRouter()
router.register('boards', viewsets.BoardViewSet, basename='board')
router.register('capabilities', viewsets.BoardCapabilityViewSet, basename='capability')

urlpatterns = [
    path('', include(router.urls)),
]

# Available endpoints (auto-generated by ViewSet):
# GET/POST    /api/v1/boards/
# GET/PUT/DELETE /api/v1/boards/{id}/
# GET         /api/v1/boards/{id}/status/
# GET         /api/v1/boards/{id}/capabilities/
# POST        /api/v1/boards/{id}/capabilities/
# GET/PUT/DELETE /api/v1/boards/{board_id}/capabilities/{id}/
# GET         /api/v1/boards/{id}/logs/
# GET         /api/v1/boards/{id}/test-runs/
# POST        /api/v1/boards/{id}/lock/
# POST        /api/v1/boards/{id}/unlock/
```

### Test Execution Endpoints

```python
# apps/test_execution/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = 'test_execution'

router = DefaultRouter()
router.register('test-runs', viewsets.TestRunViewSet, basename='testrun')

urlpatterns = [
    path('', include(router.urls)),
]

# Available endpoints:
# GET/POST    /api/v1/test-runs/
# GET/DELETE  /api/v1/test-runs/{id}/
# POST        /api/v1/test-runs/{id}/pause/
# POST        /api/v1/test-runs/{id}/resume/
# POST        /api/v1/test-runs/{id}/kill/
# GET         /api/v1/test-runs/{id}/logs/
# GET         /api/v1/test-runs/{id}/results/
# GET         /api/v1/test-runs/{id}/status-stream/
# POST        /api/v1/test-runs/{id}/retry/
```

---

## UART Communication Implementation

### UART Handler

```python
# apps/test_execution/uart/handler.py

import serial
import threading
import logging
from queue import Queue, Empty
from typing import Optional, Callable, Dict
from django.utils import timezone
from .protocol import MessageType
from .checksums import CRC16

logger = logging.getLogger(__name__)

class UARTHandler:
    """Manages UART communication with hardware boards"""
    
    def __init__(self, board, on_message_callback: Optional[Callable] = None):
        self.board = board
        self.serial_conn = None
        self.message_queue = Queue()
        self.read_thread = None
        self.write_lock = threading.Lock()
        self.is_running = False
        self.on_message_callback = on_message_callback
    
    def connect(self) -> bool:
        """Open UART connection"""
        try:
            self.serial_conn = serial.Serial(
                port=self.board.uart_port,
                baudrate=self.board.baud_rate,
                bytesize=self.board.data_bits,
                stopbits=self.board.stop_bits,
                parity=self.board.parity,
                rtscts=self.board.flow_control,
                timeout=1.0,
                write_timeout=1.0,
            )
            
            if self.serial_conn.is_open:
                self.is_running = True
                self.read_thread = threading.Thread(
                    target=self._read_loop,
                    daemon=True,
                    name=f"UART-Read-{self.board.id}"
                )
                self.read_thread.start()
                
                logger.info(
                    f"Connected to board {self.board.name} "
                    f"on {self.board.uart_port} @ {self.board.baud_rate}bps"
                )
                return True
            else:
                logger.error(f"Failed to open UART port {self.board.uart_port}")
                return False
        
        except serial.SerialException as e:
            logger.error(f"Serial port error: {e}")
            self.board.log_error(f"UART connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close UART connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.is_running = False
            try:
                self.serial_conn.close()
            except Exception as e:
                logger.error(f"Error closing serial port: {e}")
            
            if self.read_thread:
                self.read_thread.join(timeout=2)
            
            logger.info(f"Disconnected from board {self.board.name}")
    
    def send_message(self, message_type: str, payload: Dict = None) -> bool:
        """Send message to board"""
        with self.write_lock:
            try:
                message = self._format_message(message_type, payload or {})
                self.serial_conn.write(message.encode('utf-8') + b'\r\n')
                logger.debug(f"Sent to {self.board.name}: {message}")
                return True
            except Exception as e:
                logger.error(f"Failed to send message: {e}")
                return False
    
    def _read_loop(self):
        """Background thread: continuously read from UART"""
        buffer = ""
        
        while self.is_running:
            try:
                if self.serial_conn.in_waiting:
                    byte_data = self.serial_conn.read()
                    char = byte_data.decode('utf-8', errors='ignore')
                    
                    if char == '\n':
                        if buffer.strip():
                            self.message_queue.put(buffer.strip())
                            if self.on_message_callback:
                                try:
                                    self.on_message_callback(buffer.strip())
                                except Exception as e:
                                    logger.error(f"Callback error: {e}")
                        buffer = ""
                    elif char != '\r':
                        buffer += char
            
            except Exception as e:
                logger.error(f"Read loop error: {e}")
                break
    
    def get_message(self, timeout=1.0) -> Optional[str]:
        """Get next message from queue"""
        try:
            return self.message_queue.get(timeout=timeout)
        except Empty:
            return None
    
    def _format_message(self, msg_type: str, payload: Dict) -> str:
        """Format message with checksum"""
        parts = [msg_type]
        for key in sorted(payload.keys()):
            parts.append(str(payload[key]))
        
        message = ','.join(parts)
        checksum = CRC16.calculate(message)
        
        return f"{message},{checksum:04X}"
    
    def is_connected(self) -> bool:
        """Check if UART is connected"""
        return (self.serial_conn is not None and 
                self.serial_conn.is_open and 
                self.is_running)
```

### Message Parser

```python
# apps/test_execution/uart/parser.py

import json
from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MessageParser:
    """Parse incoming UART messages"""
    
    @staticmethod
    def parse(raw_message: str) -> Optional[Dict]:
        """Parse raw UART message"""
        if not raw_message or ',' not in raw_message:
            return None
        
        try:
            parts = raw_message.split(',')
            msg_type = parts[0]
            
            if msg_type == 'HEARTBEAT':
                return MessageParser._parse_heartbeat(parts)
            elif msg_type == 'TEST_START':
                return MessageParser._parse_test_start(parts)
            elif msg_type == 'TEST_LOG':
                return MessageParser._parse_test_log(parts)
            elif msg_type == 'ASSERTION':
                return MessageParser._parse_assertion(parts)
            elif msg_type == 'TEST_END':
                return MessageParser._parse_test_end(parts)
            elif msg_type == 'STATUS':
                return MessageParser._parse_status(parts)
            else:
                logger.warning(f"Unknown message type: {msg_type}")
                return None
        
        except (ValueError, IndexError) as e:
            logger.error(f"Parse error: {e}")
            return None
    
    @staticmethod
    def _parse_heartbeat(parts: list) -> Dict:
        """Parse: <HEARTBEAT>,<ID>,<TS>,<STATUS>,<CPU>,<TEMP>,<CHECKSUM>"""
        return {
            'type': 'HEARTBEAT',
            'board_id': parts[1],
            'timestamp': int(parts[2]),
            'status': parts[3],
            'cpu_load': float(parts[4]),
            'temperature': float(parts[5]) if len(parts) > 5 else None,
        }
    
    @staticmethod
    def _parse_test_start(parts: list) -> Dict:
        """Parse: <TEST_START>,<ID>,<TESTRUN_ID>,<TIMESTAMP>,<CHECKSUM>"""
        return {
            'type': 'TEST_START',
            'board_id': parts[1],
            'testrun_id': int(parts[2]),
            'timestamp': int(parts[3]),
        }
    
    @staticmethod
    def _parse_test_log(parts: list) -> Dict:
        """Parse: <TEST_LOG>,<ID>,<TESTRUN_ID>,<LEVEL>,<MESSAGE>,...,<CHECKSUM>"""
        return {
            'type': 'TEST_LOG',
            'board_id': parts[1],
            'testrun_id': int(parts[2]),
            'level': parts[3],
            'message': ','.join(parts[4:-1]),  # Message may contain commas
            'timestamp': datetime.utcnow().isoformat(),
        }
    
    @staticmethod
    def _parse_assertion(parts: list) -> Dict:
        """Parse: <ASSERTION>,<ID>,<TESTRUN_ID>,<RESULT>,<NAME>,<EXPECTED>,<ACTUAL>,...,<CHECKSUM>"""
        return {
            'type': 'ASSERTION',
            'board_id': parts[1],
            'testrun_id': int(parts[2]),
            'result': parts[3],
            'assertion_name': parts[4],
            'expected': parts[5],
            'actual': parts[6],
            'details': ','.join(parts[7:-1]) if len(parts) > 8 else '',
        }
    
    @staticmethod
    def _parse_test_end(parts: list) -> Dict:
        """Parse: <TEST_END>,<ID>,<TESTRUN_ID>,<EXIT_CODE>,<DURATION>,<SUMMARY>,...,<CHECKSUM>"""
        return {
            'type': 'TEST_END',
            'board_id': parts[1],
            'testrun_id': int(parts[2]),
            'exit_code': int(parts[3]),
            'duration': int(parts[4]),
            'summary': parts[5] if len(parts) > 5 else 'PASSED',
            'details': ','.join(parts[6:-1]) if len(parts) > 7 else '',
        }
    
    @staticmethod
    def _parse_status(parts: list) -> Dict:
        """Parse: <STATUS>,<ID>,<STATE>,<ERROR_CODE>,<MESSAGE>,...,<CHECKSUM>"""
        return {
            'type': 'STATUS',
            'board_id': parts[1],
            'state': parts[2],
            'error_code': parts[3] if len(parts) > 3 else '',
            'message': ','.join(parts[4:-1]) if len(parts) > 5 else '',
        }
```

---

## Test Execution Engine

### Core Executor

```python
# apps/test_execution/execution/executor.py

import logging
from typing import Dict, Tuple
from django.utils import timezone
from django.db import transaction
from apps.test_execution.models import TestRun, TestResult
from apps.test_execution.uart.handler import UARTHandler
from apps.test_execution.uart.parser import MessageParser
from apps.realtime.handlers.pusher import PusherHandler

logger = logging.getLogger(__name__)

class TestExecutor:
    """Core test execution engine"""
    
    def __init__(self, testrun: TestRun):
        self.testrun = testrun
        self.board = testrun.board
        self.uart = None
        self.pusher = PusherHandler()
    
    def execute(self) -> Tuple[bool, str]:
        """Execute test and return (success, message)"""
        try:
            # Validate execution can proceed
            can_execute, reason = self.board.can_execute_test()
            if not can_execute:
                return False, reason
            
            # Initialize UART
            self.uart = UARTHandler(
                self.board,
                on_message_callback=self._handle_uart_message
            )
            
            if not self.uart.connect():
                return False, "Failed to connect to board"
            
            try:
                # Update testrun status
                with transaction.atomic():
                    self.testrun.status = 'IN_PROGRESS'
                    self.testrun.start_time = timezone.now()
                    self.testrun.save()
                
                self.pusher.publish_testrun_update(self.testrun)
                
                # Send test script to board
                self._send_test_script()
                
                # Wait for completion
                success = self._wait_for_completion()
                
                return success, "Test execution completed"
            
            finally:
                self.uart.disconnect()
        
        except Exception as e:
            logger.error(f"Test execution error: {e}", exc_info=True)
            self._handle_execution_error(str(e))
            return False, str(e)
    
    def _send_test_script(self):
        """Send test script to board"""
        script_data = self.testrun.test_case.script_content
        script_hash = hash(script_data)
        
        self.uart.send_message('EXEC_TEST', {
            'testrun_id': self.testrun.id,
            'script_hash': script_hash,
            'script_size': len(script_data)
        })
        
        logger.info(f"Sent test script to board {self.board.name}")
    
    def _wait_for_completion(self, timeout=3600) -> bool:
        """Wait for test to complete"""
        start_time = timezone.now()
        
        while True:
            message = self.uart.get_message(timeout=5)
            
            if message:
                parsed = MessageParser.parse(message)
                if parsed:
                    self._process_message(parsed)
            
            # Check for timeout
            elapsed = (timezone.now() - start_time).total_seconds()
            if elapsed > timeout:
                self.testrun.status = 'FAILED'
                self.testrun.error_message = 'Test execution timeout'
                self.testrun.save()
                logger.error(f"Test {self.testrun.id} timed out")
                return False
            
            # Check if test completed
            if self.testrun.status in ['COMPLETED', 'FAILED', 'KILLED', 'ERROR']:
                return self.testrun.status == 'COMPLETED'
        
        return False
    
    def _handle_uart_message(self, message: str):
        """Callback for UART message"""
        parsed = MessageParser.parse(message)
        if parsed:
            self._process_message(parsed)
    
    def _process_message(self, parsed: Dict):
        """Process parsed message"""
        msg_type = parsed.get('type')
        
        if msg_type == 'TEST_LOG':
            self._handle_log(parsed)
        elif msg_type == 'ASSERTION':
            self._handle_assertion(parsed)
        elif msg_type == 'TEST_END':
            self._handle_test_end(parsed)
        elif msg_type == 'HEARTBEAT':
            self._handle_heartbeat(parsed)
    
    def _handle_log(self, data: Dict):
        """Handle test log line"""
        message = data['message']
        level = data['level']
        
        # Append to log
        self.testrun.stdout_log += f"[{level}] {message}\n"
        self.testrun.save(update_fields=['stdout_log'])
        
        # Publish to real-time
        self.pusher.publish_log_line(self.testrun, message)
    
    def _handle_assertion(self, data: Dict):
        """Handle assertion result"""
        with transaction.atomic():
            TestResult.objects.create(
                test_run=self.testrun,
                assertion_name=data['assertion_name'],
                expected_value=data['expected'],
                actual_value=data['actual'],
                result_type='PASSED' if data['result'] == 'PASSED' else 'FAILED',
                execution_time=0
            )
    
    def _handle_test_end(self, data: Dict):
        """Handle test completion"""
        self.testrun.status = 'COMPLETED' if data['exit_code'] == 0 else 'FAILED'
        self.testrun.exit_code = data['exit_code']
        self.testrun.end_time = timezone.now()
        self.testrun.duration = self.testrun.end_time - self.testrun.start_time
        self.testrun.result_summary = {
            'summary': data.get('summary'),
            'duration_seconds': int(self.testrun.duration.total_seconds())
        }
        self.testrun.save()
        
        self.pusher.publish_testrun_update(self.testrun)
    
    def _handle_heartbeat(self, data: Dict):
        """Handle board heartbeat"""
        self.board.update_heartbeat(data.get('status', 'IDLE'))
    
    def _handle_execution_error(self, error_message: str):
        """Handle execution error"""
        self.testrun.status = 'ERROR'
        self.testrun.error_message = error_message
        self.testrun.end_time = timezone.now()
        self.testrun.save()
        self.pusher.publish_testrun_update(self.testrun)
        self.board.log_error(error_message)
```

---

## Celery Tasks

### Test Execution Tasks

```python
# apps/test_execution/tasks.py

from celery import shared_task
from django.utils import timezone
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def execute_test(self, testrun_id):
    """Execute test on board"""
    try:
        from apps.test_execution.models import TestRun
        from apps.test_execution.execution.executor import TestExecutor
        
        testrun = TestRun.objects.get(id=testrun_id)
        executor = TestExecutor(testrun)
        
        success, message = executor.execute()
        
        if not success:
            logger.error(f"Test {testrun_id} failed: {message}")
        
        return {'status': 'success' if success else 'failed', 'message': message}
    
    except TestRun.DoesNotExist:
        logger.error(f"TestRun {testrun_id} not found")
        return {'status': 'failed', 'message': 'TestRun not found'}
    except Exception as exc:
        logger.error(f"Unexpected error in execute_test: {exc}", exc_info=True)
        raise self.retry(exc=exc, countdown=60)


@shared_task
def monitor_board_heartbeat(board_id):
    """Monitor board heartbeat status"""
    from apps.boards.models import Board
    from apps.realtime.handlers.pusher import PusherHandler
    
    try:
        board = Board.objects.get(id=board_id)
        
        # Check if board should be offline
        if not board.is_online and board.connection_status != 'OFFLINE':
            board.connection_status = 'OFFLINE'
            board.save()
            
            PusherHandler().publish_board_status(board)
            board.log_error('Board went offline (no heartbeat)')
    
    except Board.DoesNotExist:
        pass


@shared_task
def sync_board_status():
    """Sync all board statuses periodically"""
    from apps.boards.models import Board
    
    boards = Board.objects.filter(is_active=True)
    for board in boards:
        if not board.is_online and board.connection_status != 'OFFLINE':
            monitor_board_heartbeat.delay(board.id)


@shared_task
def cleanup_old_logs(days=30):
    """Delete old test logs to free up space"""
    from apps.test_execution.models import TestRun
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=days)
    old_runs = TestRun.objects.filter(created_at__lt=cutoff_date)
    
    count = old_runs.count()
    old_runs.delete()
    
    logger.info(f"Deleted {count} old test runs")
    return {'deleted': count}
```

---

## Django Channels WebSocket Consumers

### Real-Time Consumers

```python
# apps/realtime/consumers.py

import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class TestRunConsumer(AsyncWebsocketConsumer):
    """Handle real-time test run updates"""
    
    async def connect(self):
        self.testrun_id = self.scope['url_route']['kwargs']['testrun_id']
        self.user = self.scope['user']
        self.room_name = f'testrun_{self.testrun_id}'
        
        # Verify permission
        if not await self.has_permission():
            await self.close()
            return
        
        # Join room
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()
        
        logger.info(f"User {self.user.id} connected to testrun {self.testrun_id}")
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        logger.info(f"User disconnected from testrun {self.testrun_id}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            command = data.get('command')
            
            if command == 'pause':
                await self.pause_test()
            elif command == 'resume':
                await self.resume_test()
            elif command == 'kill':
                await self.kill_test()
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
    
    async def testrun_update(self, event):
        """Send test run update to WebSocket"""
        await self.send(text_data=json.dumps(event['data']))
    
    async def testrun_log(self, event):
        """Send test log line to WebSocket"""
        await self.send(text_data=json.dumps(event['data']))
    
    @database_sync_to_async
    def has_permission(self):
        """Verify user can access this test run"""
        try:
            from apps.test_execution.models import TestRun
            testrun = TestRun.objects.get(id=self.testrun_id)
            return (
                testrun.initiated_by == self.user or
                self.user.is_admin
            )
        except TestRun.DoesNotExist:
            return False
    
    @database_sync_to_async
    def pause_test(self):
        """Pause test execution"""
        from apps.test_execution.models import TestRun
        from apps.test_execution.uart.handler import UARTHandler
        
        try:
            testrun = TestRun.objects.get(id=self.testrun_id)
            if testrun.can_pause():
                testrun.status = 'PAUSED'
                testrun.save()
                
                logger.info(f"Test {self.testrun_id} paused by {self.user.email}")
        except TestRun.DoesNotExist:
            pass
    
    @database_sync_to_async
    def kill_test(self):
        """Kill test execution"""
        from apps.test_execution.models import TestRun
        
        try:
            testrun = TestRun.objects.get(id=self.testrun_id)
            if testrun.can_kill():
                testrun.status = 'KILLED'
                testrun.end_time = timezone.now()
                testrun.save()
                
                logger.info(f"Test {self.testrun_id} killed by {self.user.email}")
        except TestRun.DoesNotExist:
            pass


class BoardStatusConsumer(AsyncWebsocketConsumer):
    """Handle board status updates"""
    
    async def connect(self):
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.user = self.scope['user']
        
        if not await self.has_permission():
            await self.close()
            return
        
        self.room_name = f'board_{self.board_id}_status'
        
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
    
    async def board_status_update(self, event):
        """Send board status update"""
        await self.send(text_data=json.dumps(event['data']))
    
    @database_sync_to_async
    def has_permission(self):
        """Verify user can access this board"""
        from apps.boards.models import Board
        try:
            board = Board.objects.get(id=self.board_id)
            return self.user.has_board_access(board)
        except Board.DoesNotExist:
            return False
```

---

## Settings Configuration

### Base Settings

```python
# config/settings/base.py

import os
from pathlib import Path
from datetime import timedelta
import logging.config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'dev-secret-key-change-in-production'
)

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',
    'corsheaders',
    'django_filters',
    
    # Local apps
    'apps.authentication',
    'apps.boards',
    'apps.test_cases',
    'apps.test_execution',
    'apps.realtime',
    'apps.dashboard',
    'apps.configuration',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'test_management'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
    }
}

# Redis configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
        }
    }
}

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

# Custom user model
AUTH_USER_MODEL = 'authentication.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    },
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://localhost:8000'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    'monitor-boards': {
        'task': 'apps.test_execution.tasks.sync_board_status',
        'schedule': timedelta(seconds=30),
    },
    'cleanup-logs': {
        'task': 'apps.test_execution.tasks.cleanup_old_logs',
        'schedule': timedelta(days=1),
    },
}

# Pusher Configuration
PUSHER_APP_ID = os.getenv('PUSHER_APP_ID', '')
PUSHER_KEY = os.getenv('PUSHER_KEY', '')
PUSHER_SECRET = os.getenv('PUSHER_SECRET', '')
PUSHER_CLUSTER = os.getenv('PUSHER_CLUSTER', 'mt1')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'uart_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'uart.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.test_execution.uart': {
            'handlers': ['uart_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),
    'style-src': ("'self'", "'unsafe-inline'"),
}
X_FRAME_OPTIONS = 'DENY'

# UART Configuration
UART_READ_TIMEOUT = 1.0
UART_WRITE_TIMEOUT = 1.0
UART_DEFAULT_BAUD_RATE = 115200
UART_MESSAGE_TIMEOUT = 60

# Test Execution
TEST_EXECUTION_TIMEOUT = 3600  # 1 hour
TEST_LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
```

---

## Testing Strategy

### Test Structure

```python
# tests/conftest.py

import pytest
from django.conf import settings
from django.test import override_settings
from factory import Faker
import logging

# Disable logging during tests
logging.disable(logging.CRITICAL)

@pytest.fixture
def db_setup():
    """Setup database for tests"""
    # Run migrations
    pass

@pytest.fixture
def user_factory():
    """Factory for creating test users"""
    from apps.authentication.models import User
    from factory import DjangoModelFactory
    
    class UserFactory(DjangoModelFactory):
        username = Faker('username')
        email = Faker('email')
        role = 'NORMAL_USER'
        
        class Meta:
            model = User
    
    return UserFactory

@pytest.fixture
def admin_user(user_factory):
    """Create admin user"""
    return user_factory(role='ADMIN', username='admin')

@pytest.fixture
def super_admin_user(user_factory):
    """Create super admin user"""
    return user_factory(role='SUPER_ADMIN', username='superadmin')

@pytest.fixture
def api_client():
    """DRF test client"""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user_factory):
    """Authenticated API client"""
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client, user
```

### Unit Test Example

```python
# apps/authentication/tests/test_models.py

import pytest
from apps.authentication.models import User

@pytest.mark.django_db
class TestUserModel:
    
    def test_user_creation(self):
        """Test creating a user"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPassword123'
        )
        
        assert user.email == 'test@example.com'
        assert user.is_active
        assert user.role == 'NORMAL_USER'
    
    def test_super_admin_creation(self):
        """Test creating super admin"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='AdminPass123'
        )
        
        assert user.is_super_admin
        assert user.is_admin
        assert user.is_staff
        assert user.is_superuser
    
    def test_board_access_control(self, user_factory):
        """Test board access control"""
        user = user_factory(role='NORMAL_USER')
        board = ... # Create board
        
        assert not user.has_board_access(board)
        
        user.assigned_boards.add(board)
        assert user.has_board_access(board)
```

### API Test Example

```python
# apps/boards/tests/test_viewsets.py

import pytest
from rest_framework import status

@pytest.mark.django_db
class TestBoardViewSet:
    
    def test_list_boards_authenticated(self, authenticated_client):
        """Test listing boards for authenticated user"""
        client, user = authenticated_client
        
        response = client.get('/api/v1/boards/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_create_board_admin_only(self, api_client, admin_user):
        """Test creating board requires admin"""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'name': 'Test Board',
            'serial_number': 'SN12345',
            'uart_port': '/dev/ttyUSB0',
        }
        
        response = api_client.post('/api/v1/boards/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_create_board_unauthorized(self, authenticated_client):
        """Test normal user cannot create board"""
        client, user = authenticated_client
        
        data = {
            'name': 'Test Board',
            'serial_number': 'SN12345',
            'uart_port': '/dev/ttyUSB0',
        }
        
        response = client.post('/api/v1/boards/', data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
```

---

## Deployment Configuration

### Docker Setup

```dockerfile
# docker/Dockerfile

FROM python:3.11-slim

WORKDIR /code

# System dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements/production.txt .
RUN pip install --no-cache-dir -r production.txt

# Application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 app && chown -R app:app /code
USER app

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]
```

### Docker Compose

```yaml
# docker-compose.prod.yml

version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test_management_prod
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: .
      dockerfile: docker/Dockerfile
    command: >
      sh -c "python manage.py migrate &&
             gunicorn config.wsgi -w 4 -b 0.0.0.0:8000"
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  celery:
    build:
      context: .
      dockerfile: docker/Dockerfile
    command: celery -A config worker -l info
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis
    restart: unless-stopped

  celery-beat:
    build:
      context: .
      dockerfile: docker/Dockerfile
    command: celery -A config beat -l info
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/2
    depends_on:
      - db
      - redis
    restart: unless-stopped

  daphne:
    build:
      context: .
      dockerfile: docker/Dockerfile
    command: daphne -b 0.0.0.0 -p 8001 config.asgi:application
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./staticfiles:/code/staticfiles:ro
      - ./media:/code/media:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
      - daphne
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

This completes the Django backend specification. It covers all aspects of backend development including models, APIs, UART communication, real-time updates, celery tasks, testing, and deployment.

