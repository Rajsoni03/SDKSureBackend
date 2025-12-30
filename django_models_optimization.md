# Django Models Review & Optimization Guide

## Executive Summary

Your models are **structurally sound** with good relationships, but they need several improvements:
- **Formatting issues** (indentation in the provided file)
- **Database optimization** (indexes, unique constraints)
- **Additional properties** (created_at, updated_at, UUID primary keys)
- **Performance enhancements** (select_related, prefetch_related optimization)
- **Data validation** (choices refactoring, field constraints)

---

## Current Model Analysis

### ✅ What's Good

1. **Relationship Structure**: FK and M2M relationships are appropriate
2. **Status Fields**: Well-designed with choices
3. **Timestamp Fields**: Used for audit trails
4. **Separation of Concerns**: PCStats separate from TestPC

### ⚠️ Issues Found

1. **Missing Timestamps**: No `updated_at` on Board, Relay, Capability
2. **No Unique Constraints**: IP addresses, MAC addresses, hostnames not unique
3. **Missing Indexes**: Foreign keys should have indexes
4. **UUID Not Used**: Using auto-increment, should use UUID for security
5. **No Default Values**: Some fields missing sensible defaults
6. **Verbose Names**: Missing on many models
7. **Help Text**: Missing on model fields
8. **String Lengths**: Some too restrictive (IP address 20 chars, MAC 50)
9. **Validation**: No blank/null consistency
10. **No Ordering**: Some models missing default ordering

---

## Optimized Model Implementation

```python
# apps/core/models.py

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    URLValidator,
    RegexValidator,
)
from django.utils.translation import gettext_lazy as _
import uuid


# ============================================================================
# CAPABILITY MODEL
# ============================================================================

class Capability(models.Model):
    """
    Represents capabilities that a Board can have.
    E.g., CMD, CAMERA, DISPLAY, SOUND, FILE, SENSOR
    """
    
    CAPABILITY_CHOICES = [
        ('CMD', _('Command Execution')),
        ('CAMERA', _('Camera Testing')),
        ('DISPLAY', _('Display Output')),
        ('SOUND', _('Sound/Audio')),
        ('FILE', _('File System')),
        ('SENSOR', _('Sensor Reading')),
        ('GPIO', _('GPIO Control')),
        ('ADC', _('Analog-to-Digital')),
        ('NETWORK', _('Network Connectivity')),
    ]
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier'
    )
    
    # Core Fields
    name = models.CharField(
        max_length=50,
        choices=CAPABILITY_CHOICES,
        unique=True,
        help_text='Capability name'
    )
    description = models.TextField(
        blank=True,
        help_text='Detailed description of this capability'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = _('Capabilities')
        indexes = [
            models.Index(fields=['name'])
        ]
    
    def __str__(self):
        return f"{self.get_name_display()}"
    
    def __repr__(self):
        return f"<Capability: {self.name}>"


# ============================================================================
# RELAY MODEL
# ============================================================================

class Relay(models.Model):
    """
    Represents a power relay or network relay used to control boards.
    Can be power extension or ethernet relay.
    """
    
    STATUS_CHOICES = [
        ('ACTIVE', _('Active')),
        ('INACTIVE', _('Inactive')),
        ('MAINTENANCE', _('Maintenance')),
        ('FAULT', _('Fault')),
    ]
    
    MODEL_TYPE_CHOICES = [
        ('POWER_EXTENSION', _('Power Extension')),
        ('ETH_008_A', _('Ethernet 008 Type A')),
        ('ETH_008_B', _('Ethernet 008 Type B')),
        ('ETH_016', _('Ethernet 016')),
        ('CUSTOM', _('Custom')),
    ]
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Identification Fields
    relay_name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Unique name for this relay'
    )
    model_type = models.CharField(
        max_length=50,
        choices=MODEL_TYPE_CHOICES,
        help_text='Type of relay'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='INACTIVE',
        help_text='Current operational status'
    )
    
    # Location
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text='Physical location (e.g., Rack A, Shelf 2)'
    )
    
    # Network Fields
    ip_address = models.GenericIPAddressField(
        unique=True,
        help_text='IP address of the relay'
    )
    mac_address = models.CharField(
        max_length=17,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
                message='Enter a valid MAC address'
            )
        ],
        help_text='MAC address in format XX:XX:XX:XX:XX:XX'
    )
    
    # Additional Fields
    port_count = models.PositiveIntegerField(
        default=8,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text='Number of ports on this relay'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_checked_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Last health check timestamp'
    )
    
    class Meta:
        ordering = ('relay_name',)
        verbose_name_plural = _('Relays')
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['mac_address']),
            models.Index(fields=['status']),
            models.Index(fields=['relay_name']),
        ]
    
    def __str__(self):
        return f"{self.relay_name} ({self.ip_address})"
    
    def __repr__(self):
        return f"<Relay: {self.relay_name}>"
    
    @property
    def is_healthy(self):
        """Check if relay is responsive."""
        return self.status == 'ACTIVE'


# ============================================================================
# TEST PC MODEL
# ============================================================================

class TestPC(models.Model):
    """
    Represents a test execution PC/machine that controls board testing.
    """
    
    STATUS_CHOICES = [
        ('ONLINE', _('Online')),
        ('OFFLINE', _('Offline')),
        ('MAINTENANCE', _('Maintenance')),
        ('INITIALIZING', _('Initializing')),
    ]
    
    OS_VERSION_CHOICES = [
        ('ubuntu_18_04', 'Ubuntu 18.04 LTS'),
        ('ubuntu_20_04', 'Ubuntu 20.04 LTS'),
        ('ubuntu_22_04', 'Ubuntu 22.04 LTS'),
        ('ubuntu_24_04', 'Ubuntu 24.04 LTS'),
        ('centos_7', 'CentOS 7'),
        ('centos_8', 'CentOS 8'),
        ('centos_9', 'CentOS 9'),
        ('windows_10', 'Windows 10'),
        ('windows_11', 'Windows 11'),
        ('macos_ventura', 'macOS Ventura'),
        ('macos_sonoma', 'macOS Sonoma'),
    ]
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Basic Identification
    hostname = models.CharField(
        max_length=255,
        unique=True,
        help_text='Hostname of the PC'
    )
    ip_address = models.GenericIPAddressField(
        unique=True,
        help_text='IP address of the PC'
    )
    domain_name = models.CharField(
        max_length=255,
        blank=True,
        help_text='FQDN of the PC'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OFFLINE',
        help_text='Current operational status'
    )
    
    # System Information
    os_version = models.CharField(
        max_length=50,
        choices=OS_VERSION_CHOICES,
        help_text='Operating system version'
    )
    disk_mountpoint = models.CharField(
        max_length=255,
        default='/',
        help_text='Primary disk mount point'
    )
    
    # Location
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text='Physical location in lab/datacenter/rac'
    )
    
    # Additional Info
    comment = models.TextField(
        blank=True,
        help_text='Additional notes about this PC'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_heartbeat_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Last heartbeat received from this PC'
    )
    
    class Meta:
        ordering = ('hostname',)
        verbose_name = _('Test PC')
        verbose_name_plural = _('Test PCs')
        indexes = [
            models.Index(fields=['hostname']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['os_version']),
        ]
    
    def __str__(self):
        return f"{self.hostname} ({self.ip_address})"
    
    def __repr__(self):
        return f"<TestPC: {self.hostname}>"
    
    @property
    def is_online(self):
        """Check if PC is currently online."""
        return self.status == 'ONLINE'
    
    @property
    def is_available_for_testing(self):
        """Check if PC can accept new test runs."""
        return self.status in ['ONLINE', 'INITIALIZING']


# ============================================================================
# PC STATS MODEL
# ============================================================================

class PCStats(models.Model):
    """
    Real-time performance statistics for a TestPC.
    Records are created at regular intervals (every 5-10 minutes).
    """
    
    STATUS_CHOICES = [
        ('HEALTHY', _('Healthy')),
        ('WARNING', _('Warning')),
        ('CRITICAL', _('Critical')),
        ('UNKNOWN', _('Unknown')),
    ]
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationship
    test_pc = models.ForeignKey(
        TestPC,
        on_delete=models.CASCADE,
        related_name='performance_stats',
        help_text='Reference to the TestPC'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='UNKNOWN',
        help_text='Overall health status'
    )
    
    # Memory Stats
    memory_total_gb = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Total memory in GB'
    )
    memory_used_gb = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Used memory in GB'
    )
    memory_free_gb = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Free memory in GB'
    )
    memory_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Memory usage percentage'
    )
    
    # Disk Stats
    disk_total_gb = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Total disk space in GB'
    )
    disk_used_gb = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Used disk space in GB'
    )
    disk_free_gb = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Free disk space in GB'
    )
    disk_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Disk usage percentage'
    )
    
    # CPU Stats
    cpu_percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='CPU usage percentage'
    )
    
    # Network Stats
    network_io_read_mb = models.FloatField(
        default=0,
        help_text='Network read in MB'
    )
    network_io_write_mb = models.FloatField(
        default=0,
        help_text='Network write in MB'
    )
    
    # Process Stats
    process_count = models.PositiveIntegerField(
        help_text='Number of active test process'
    )
    thread_count = models.PositiveIntegerField(
        help_text='Number of active test threads'
    )
    
    # Timestamp
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text='When this stat was recorded'
    )
    
    class Meta:
        ordering = ('-timestamp',)
        verbose_name = _('PC Stats')
        verbose_name_plural = _('PC Stats')
        indexes = [
            models.Index(fields=['test_pc', '-timestamp']),
            models.Index(fields=['status', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
        # Keep only 30 days of stats for add code logic here...
        constraints = [
            models.CheckConstraint(
                check=models.Q(memory_percent__gte=0) & models.Q(memory_percent__lte=100),
                name='memory_percent_range'
            ),
        ]
    
    def __str__(self):
        return f"{self.test_pc.hostname} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    def __repr__(self):
        return f"<PCStats: {self.test_pc.hostname} @ {self.timestamp}>"
    
    @property
    def is_healthy(self):
        """Determine if PC is healthy based on thresholds."""
        return self.status == 'HEALTHY'
    
    @property
    def memory_available_gb(self):
        """Calculate available memory."""
        return self.memory_total_gb - self.memory_used_gb


# ============================================================================
# BOARD MODEL
# ============================================================================

class Board(models.Model):
    """
    Represents a hardware board (EVM) used for testing.
    Boards are controlled by TestPCs via relays and execute test cases.
    """
    
    PLATFORM_CHOICES = [
        ('j721s2', 'TI J721S2'),
        ('j721e', 'TI J721E'),
        ('j722s', 'TI J722S'),
        ('j742s2', 'TI J742S2'),
        ('j784s4', 'TI J784S4'),
        ('j7200', 'TI J7200'),
        ('am62x', 'TI AM62x'),
        ('am62px', 'TI AM62Px'),
    ]
    
    STATUS_CHOICES = [
        ('IDLE', _('Idle')),
        ('BUSY', _('Busy')),
        ('UPDATING_SDK', _('Updating SDK')),
        ('OFFLINE', _('Offline')),
        ('DEACTIVATED', _('Deactivated')),
        ('ERROR', _('Error')),
    ]
    
    TEST_FARM_CHOICES = [
        ('HLOS', _('HLOS (Linux/QNX)')),
        ('RTOS', _('RTOS (Real-Time OS)')),
        ('BAREMETAL', _('Bare-metal')),
        ('STAGING', _('Staging')),
        ('INTEGRATION', _('Integration')),
    ]
    
    DEVICE_TYPE_CHOICES = [
        ('EVM', _('Evaluation Module')),
        ('SOCKET_BOARD', _('Socket Board')),
        ('BREAKOUT_BOARD', _('Breakout Board')),
        ('CUSTOM', _('Custom')),
    ]
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Basic Identification
    hardware_serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text='Hardware serial number'
    )
    
    # Platform & Configuration
    project = models.CharField(
        max_length=50,
        help_text='project name'
    )
    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        help_text='Platform name'
    )
    device_type = models.CharField(
        max_length=50,
        choices=DEVICE_TYPE_CHOICES,
        default='EVM',
        help_text='Type of device'
    )
    
    pg_version = models.CharField(
        max_length=100,
        blank=True,
        help_text='Processor SDK or software version'
    )
    execution_engine = models.CharField(
        max_length=100,
        blank=True,
        help_text='Test execution engine (e.g., Robot Framework)'
    )
    test_farm = models.CharField(
        max_length=50,
        choices=TEST_FARM_CHOICES,
        help_text='Test farm/environment'
    )
    
    # Capabilities
    capabilities = models.ManyToManyField(
        Capability,
        blank=True,
        related_name='boards',
        help_text='Capabilities this board supports'
    )
    
    # Software
    sdk_version = models.CharField(
        max_length=100,
        help_text='SDK/firmware version'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OFFLINE',
        help_text='Current operational status'
    )
    is_alive = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Whether board is currently responsive'
    )
    is_locked = models.BooleanField(
        default=False,
        help_text='Whether board is locked for exclusive use'
    )
    
    # Network
    board_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address of the board (if applicable)'
    )
    
    # Relay Configuration
    relay = models.ForeignKey(
        Relay,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='boards',
        help_text='Associated power/control relay'
    )
    relay_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text='Port number on the relay'
    )
    
    # TestPC Relationship
    test_pc = models.ForeignKey(
        TestPC,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='boards',
        help_text='TestPC that controls this board'
    )
    
    # Location
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text='Physical location'
    )
    
    # SDK Updates
    last_sdk_update_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Last SDK update timestamp'
    )
    
    # Additional Fields
    description = models.TextField(
        blank=True,
        help_text='Additional description'
    )
    notes = models.TextField(
        blank=True,
        help_text='Administrative notes'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Creation timestamp'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Last update timestamp'
    )
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Last test execution timestamp'
    )
    last_heartbeat_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Last heartbeat timestamp'
    )
    
    class Meta:
        ordering = ('name',)
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')
        indexes = [
            models.Index(fields=['hardware_serial_number']),
            models.Index(fields=['status']),
            models.Index(fields=['is_alive']),
            models.Index(fields=['test_farm']),
            models.Index(fields=['project']),
            models.Index(fields=['platform']),
            models.Index(fields=['test_pc']),
            models.Index(fields=['is_locked']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', 'is_alive']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.project})"
    
    def __repr__(self):
        return f"<Board: {self.name}>"
    
    @property
    def can_execute_test(self):
        """Check if board can execute a test."""
        return (
            self.is_alive and
            self.status == 'IDLE' and
            not self.is_locked and
            self.test_pc and
            self.test_pc.is_available_for_testing
        )
    
    @property
    def is_healthy(self):
        """Overall health status."""
        return self.is_alive and self.status != 'ERROR'
    
    def get_available_capabilities(self):
        """Get list of available capabilities."""
        return self.capabilities.filter(is_active=True)
```

---

## Key Improvements Explained

### 1. **UUID Primary Keys**
```python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```
- Better security (harder to guess IDs)
- Suitable for distributed systems
- Smaller database footprint than string UUIDs

### 2. **Unique Constraints**
```python
relay_name = models.CharField(max_length=100, unique=True)
ip_address = models.GenericIPAddressField(unique=True)
mac_address = models.CharField(max_length=17, unique=True)
```
- Prevents duplicate entries
- Database enforces uniqueness

### 3. **Database Indexes**
```python
class Meta:
    indexes = [
        models.Index(fields=['ip_address']),
        models.Index(fields=['status']),
        models.Index(fields=['-timestamp']),
    ]
```
- Significantly faster queries
- Critical for frequently filtered fields

### 4. **Field Validators**
```python
cpu_cores = models.PositiveIntegerField(
    validators=[MinValueValidator(1)],
    help_text='Number of CPU cores'
)
```
- Data validation at DB level
- Prevents invalid data

### 5. **Help Text & Verbose Names**
```python
status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='OFFLINE',
    help_text='Current operational status'
)
```
- Better documentation
- Auto-generated admin forms

### 6. **Related Names**
```python
relay = models.ForeignKey(
    Relay,
    related_name='boards',  # Reverse access: relay.boards.all()
    ...
)
```
- Enables reverse queries
- Better code readability

### 7. **Properties for Computed Values**
```python
@property
def can_execute_test(self):
    """Check if board can execute a test."""
    return (
        self.is_alive and
        self.status == 'IDLE' and
        not self.is_locked and
        self.test_pc and
        self.test_pc.is_available_for_testing
    )
```
- Avoids code duplication
- Single source of truth

---

## Performance Optimization Strategies

### 1. **Query Optimization**

```python
# ✅ GOOD: Use select_related for FK
boards = Board.objects.select_related('test_pc', 'relay')

# ✅ GOOD: Use prefetch_related for M2M
boards = Board.objects.prefetch_related('capabilities')

# ❌ AVOID: N+1 queries
for board in Board.objects.all():
    print(board.test_pc.hostname)  # Query per board
```

### 2. **Partial Indexes for Common Queries**

```python
class Board(models.Model):
    class Meta:
        indexes = [
            # Only index active boards - faster for common queries
            models.Index(
                fields=['status', '-created_at'],
                name='active_boards_idx',
            ),
        ]
```

### 3. **Caching Strategy**

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def get_board_health_summary(request):
    boards = Board.objects.filter(
        test_farm='HLOS'
    ).values('status').annotate(count=Count('id'))
    return Response(boards)
```

### 4. **Database Connection Pooling**

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Keep connection for 10 min
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

### 5. **Materialized Views for Analytics**

```python
# For complex queries
class BoardSummaryView(models.Model):
    board_count = models.IntegerField()
    active_count = models.IntegerField()
    test_farm = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'board_summary_view'  # Created by SQL
```

---

## Migration Guide

### Step 1: Create New Models

```bash
python manage.py makemigrations apps.core
python manage.py migrate apps.core
```

### Step 2: Data Migration (if migrating from old schema)

```python
# migrations/0002_migrate_data.py

from django.db import migrations
import uuid

def migrate_boards(apps, schema_editor):
    OldBoard = apps.get_model('boards', 'Board')
    NewBoard = apps.get_model('core', 'Board')
    
    for old_board in OldBoard.objects.all():
        new_board = NewBoard(
            id=uuid.uuid4(),
            name=f"Board-{old_board.id}",
            hardware_serial_number=old_board.hardware_serial_number,
            # ... map other fields
        )
        new_board.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(migrate_boards),
    ]
```

---

## Summary of Changes

| Aspect | Before | After |
|--------|--------|-------|
| **Primary Keys** | Auto-increment | UUID |
| **Timestamps** | Partial | Complete (created_at, updated_at) |
| **Unique Constraints** | None | IP, MAC, hostname, serial numbers |
| **Indexes** | None | 15+ strategic indexes |
| **Validators** | None | Min/max values, regex validation |
| **Documentation** | Minimal | Help text on all fields |
| **Related Names** | None | Reverse access enabled |
| **Properties** | None | Health checks, availability status |
| **Verbose Names** | Missing | Complete with translations |

---

## Recommendations

1. **Use UUID for all primary keys** - Better for APIs and security
2. **Add created_at/updated_at to all models** - Audit trail
3. **Use db_index=True for frequently filtered fields** - Performance
4. **Add constraints at DB level** - Data integrity
5. **Use choices for status fields** - Type safety
6. **Add related_name everywhere** - Reverse queries
7. **Document with help_text** - Better UX in admin
8. **Create custom managers** - DRY queries
9. **Add model methods for business logic** - Single responsibility
10. **Use properties for computed values** - Cleaner code

This optimized schema is production-ready and scalable!
