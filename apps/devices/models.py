"""Hardware board and infrastructure models."""
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as lazt_load


class Capability(models.Model):
    """Represents a capability that a board can support."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier")
    name = models.CharField(max_length=100, unique=True, help_text="Capability name")
    description = models.TextField(blank=True, help_text="Detailed description of this capability")
    is_active = models.BooleanField(default=True, help_text="Whether this capability can be used")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = lazt_load("Capabilities")
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Capability: {self.name} - {'Active' if self.is_active else 'Inactive'}>"


class Relay(models.Model):
    """Represents a power or network relay used to control boards."""

    STATUS_CHOICES = [
        ("ACTIVE", lazt_load("Active")),
        ("INACTIVE", lazt_load("Inactive")),
        ("MAINTENANCE", lazt_load("Maintenance")),
        ("FAULT", lazt_load("Fault")),
    ]

    MODEL_TYPE_CHOICES = [
        ("POWER_EXTENSION", lazt_load("Power Extension")),
        ("ETH_008_A", lazt_load("Ethernet 008 Type A")),
        ("ETH_008_B", lazt_load("Ethernet 008 Type B")),
        ("CUSTOM", lazt_load("Custom")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    relay_name = models.CharField(max_length=100, unique=True, help_text="Unique name for this relay")
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES, help_text="Type of relay")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="INACTIVE", help_text="Relay status")
    location = models.CharField(max_length=200, blank=True, help_text="Physical location (e.g., Rack A, Shelf 2)")
    ip_address = models.GenericIPAddressField(unique=True, help_text="IP address of the relay")
    username = models.CharField(max_length=100, blank=True, help_text="Username for relay access")
    password = models.CharField(max_length=100, blank=True, help_text="Password for relay access")
    port_count = models.PositiveIntegerField(
        default=8,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Number of ports on this relay",
    )
    notes = models.TextField(blank=True, help_text="Additional notes about this relay")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_checked_at = models.DateTimeField(null=True, blank=True, help_text="Last health check timestamp")

    class Meta:
        ordering = ("relay_name",)
        verbose_name_plural = lazt_load("Relays")
        indexes = [
            models.Index(fields=["ip_address"]),
            models.Index(fields=["status"]),
            models.Index(fields=["relay_name"]),
        ]

    def __str__(self):
        return f"{self.relay_name} ({self.ip_address})"

    def __repr__(self):
        return f"<Relay: {self.relay_name} - {self.status}>"

    @property
    def is_healthy(self):
        return self.status == "ACTIVE"


class Workstation(models.Model):
    """Represents a test execution Workstation/PC."""

    STATUS_CHOICES = [
        ("ONLINE", lazt_load("Online")),
        ("OFFLINE", lazt_load("Offline")),
        ("MAINTENANCE", lazt_load("Maintenance")),
        ("INITIALIZING", lazt_load("Initializing")),
    ]

    OS_VERSION_CHOICES = [
        ("ubuntu_18_04", lazt_load("Ubuntu 18.04 LTS")),
        ("ubuntu_20_04", lazt_load("Ubuntu 20.04 LTS")),
        ("ubuntu_22_04", lazt_load("Ubuntu 22.04 LTS")),
        ("ubuntu_24_04", lazt_load("Ubuntu 24.04 LTS")),
        ("centos_7", lazt_load("CentOS 7")),
        ("centos_8", lazt_load("CentOS 8")),
        ("centos_9", lazt_load("CentOS 9")),
        ("windows", lazt_load("Windows")),
        ("macos", lazt_load("macOS")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hostname = models.CharField(max_length=255, unique=True, help_text="Hostname of the Workstation")
    ip_address = models.GenericIPAddressField(unique=True, help_text="IP address of the Workstation")
    domain_name = models.CharField(max_length=255, blank=True, help_text="FQDN of the Workstation")
    auth_token = models.CharField(max_length=200, blank=True, default="", help_text="Token used to authenticate with the Workstation")
    workarea = models.CharField(max_length=50, blank=True, default="", help_text="Logical work area name/location")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OFFLINE", help_text="Workstation status")
    os_version = models.CharField(max_length=50, choices=OS_VERSION_CHOICES, default="ubuntu_22.04", help_text="Operating system version")
    disk_mountpoint = models.CharField(max_length=255, default="/", help_text="Primary disk mount point")
    location = models.CharField(max_length=255, blank=True, help_text="Physical location in lab/datacenter/rack")
    cpu_utilization = models.FloatField(default=0, help_text="Current CPU load percentage")
    ram_utilization = models.FloatField(default=0, help_text="Current RAM load percentage")
    disk_utilization = models.FloatField(default=0, help_text="Current disk load percentage")
    docker_container_count = models.PositiveIntegerField(default=0, help_text="Number of active Docker containers")
    notes = models.TextField(blank=True, help_text="Additional notes about this Workstation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_heartbeat_at = models.DateTimeField(null=True, blank=True, help_text="Last heartbeat received from this Workstation")

    class Meta:
        ordering = ("hostname",)
        verbose_name = lazt_load("Workstation")
        verbose_name_plural = lazt_load("Workstations")
        indexes = [
            models.Index(fields=["hostname"]),
            models.Index(fields=["ip_address"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["os_version"]),
        ]

    def __str__(self):
        return f"{self.hostname} ({self.ip_address})"

    def __repr__(self):
        return f"<Workstation: {self.hostname}>"

    @property
    def is_online(self):
        return self.status == "ONLINE"

    @property
    def is_available_for_testing(self):
        return self.status == "ONLINE" and self.cpu_utilization < 80 and self.ram_utilization < 80 and self.disk_utilization < 80


class Board(models.Model): 
    """Hardware board (EVM) model."""

    PLATFORM_CHOICES = [
        ("j721s2", lazt_load("TI J721S2")),
        ("j721e", lazt_load("TI J721E")),
        ("j722s", lazt_load("TI J722S")),
        ("j742s2", lazt_load("TI J742S2")),
        ("j784s4", lazt_load("TI J784S4")),
        ("j7200", lazt_load("TI J7200")),
        ("am62a", lazt_load("TI AM62A"))
    ]

    STATUS_CHOICES = [
        ("IDLE", lazt_load("Idle")),
        ("BUSY", lazt_load("Busy")),
        ("FLASHING", lazt_load("Flashing / Updating SDK")),
        ("OFFLINE", lazt_load("Offline")),
        ("DEACTIVATED", lazt_load("Deactivated")),
        ("ERROR", lazt_load("Error")),
    ]

    TEST_FARM_CHOICES = [
        ("HLOS", lazt_load("HLOS (Linux/QNX)")),
        ("RTOS", lazt_load("RTOS (Real-Time OS)")),
        ("BAREMETAL", lazt_load("Bare-metal")),
        ("STAGING", lazt_load("Staging")),
        ("INTEGRATION", lazt_load("Integration")),
    ]

    DEVICE_TYPE_CHOICES = [
        ("EVM", lazt_load("EVM (Evaluation Module)")),
        ("HSFS", lazt_load("HSFS (High Security - Field Securable)")),
        ("HSSE", lazt_load("HSSE (High Security - Security Enforced)")),
        ("CUSTOM", lazt_load("Custom")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True, help_text="Human readable board name")
    hardware_serial_number = models.CharField(max_length=100, unique=True, help_text="Hardware serial number")
    project = models.CharField(max_length=50, help_text="Project name")
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, help_text="Platform name")
    device_type = models.CharField(
        max_length=50,
        choices=DEVICE_TYPE_CHOICES,
        default="EVM",
        help_text="Type of device"
    )
    pg_version = models.CharField(max_length=100, blank=True, help_text="Processor SDK or software version")
    test_farm = models.CharField(max_length=50, choices=TEST_FARM_CHOICES, help_text="Test farm/environment")
    capabilities = models.ManyToManyField(
        Capability,
        blank=True,
        related_name="boards",
        help_text="Capabilities this board supports",
    )
    sdk_version = models.CharField(max_length=100, help_text="SDK/firmware version")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OFFLINE", help_text="Board status")
    is_alive = models.BooleanField(default=False, db_index=True, help_text="Whether board is responsive")
    is_locked = models.BooleanField(default=False, help_text="Whether board is locked for exclusive use")
    board_ip = models.GenericIPAddressField(null=True, blank=True, help_text="IP address of the board")
    relay = models.ForeignKey(
        Relay,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="boards",
        help_text="Associated power/control relay",
    )
    relay_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Port number on the relay",
    )
    workstation = models.ForeignKey(
        Workstation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="boards",
        help_text="Workstation that controls this board",
    )
    location = models.CharField(max_length=255, blank=True, help_text="Physical location")
    last_sdk_update_at = models.DateTimeField(null=True, blank=True, help_text="Last SDK update timestamp")
    description = models.TextField(blank=True, help_text="Additional description")
    notes = models.TextField(blank=True, help_text="Administrative notes")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update timestamp")
    last_used_at = models.DateTimeField(null=True, blank=True, help_text="Last test execution timestamp")
    last_heartbeat_at = models.DateTimeField(null=True, blank=True, help_text="Last heartbeat timestamp")

    class Meta:
        ordering = ("name",)
        verbose_name = lazt_load("Board")
        verbose_name_plural = lazt_load("Boards")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["hardware_serial_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_alive"]),
            models.Index(fields=["test_farm"]),
            models.Index(fields=["project"]),
            models.Index(fields=["platform"]),
            models.Index(fields=["workstation"]),
            models.Index(fields=["is_locked"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status", "is_alive"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.project})"

    def __repr__(self):
        return f"<Board: {self.name}>"

    @property
    def can_execute_test(self):
        return (
            self.is_alive
            and self.status == "IDLE"
            and not self.is_locked
            and self.workstation
            and self.workstation.is_available_for_testing
        )

    @property
    def is_healthy(self):
        return self.is_alive and self.status != "ERROR"

    def get_available_capabilities(self):
        return self.capabilities.filter(is_active=True)

    def mark_seen(self):
        self.last_heartbeat_at = timezone.now()
        self.save(update_fields=["last_heartbeat_at"])


# class WorkstationStats(models.Model):
#     """Performance statistics for a Workstation."""

#     STATUS_CHOICES = [
#         ("HEALTHY", lazt_load("Healthy")),
#         ("WARNING", lazt_load("Warning")),
#         ("CRITICAL", lazt_load("Critical")),
#         ("UNKNOWN", lazt_load("Unknown")),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     workstation = models.ForeignKey(
#         Workstation,
#         on_delete=models.CASCADE,
#         related_name="performance_stats",
#         help_text="Reference to the Workstation these stats belong to",
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="UNKNOWN", help_text="Overall health")
#     memory_total_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Total memory in GB")
#     memory_used_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Used memory in GB")
#     memory_free_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Free memory in GB")
#     memory_percent = models.PositiveIntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)],
#         help_text="Memory usage percentage",
#     )
#     disk_total_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Total disk space in GB")
#     disk_used_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Used disk space in GB")
#     disk_free_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Free disk space in GB")
#     disk_percent = models.PositiveIntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)],
#         help_text="Disk usage percentage",
#     )
#     cpu_percent = models.FloatField(default=0, help_text="CPU usage percentage")
#     network_io_read_mb = models.FloatField(default=0, help_text="Network read in MB")
#     network_io_write_mb = models.FloatField(default=0, help_text="Network write in MB")
#     process_count = models.PositiveIntegerField(help_text="Number of active test processes")
#     thread_count = models.PositiveIntegerField(help_text="Number of active test threads")
#     timestamp = models.DateTimeField(auto_now_add=True, db_index=True, help_text="When this stat was recorded")

#     class Meta:
#         ordering = ("-timestamp",)
#         verbose_name = lazt_load("PC Stats")
#         verbose_name_plural = lazt_load("Workstation Stats")
#         indexes = [
#             models.Index(fields=["workstation", "-timestamp"]),
#             models.Index(fields=["status", "-timestamp"]),
#             models.Index(fields=["-timestamp"]),
#         ]
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(memory_percent__gte=0) & models.Q(memory_percent__lte=100),
#                 name="memory_percent_range",
#             ),
#         ]

#     def __str__(self):
#         return f"{self.workstation.hostname} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

#     def __repr__(self):
#         return f"<WorkstationStats: {self.workstation.hostname} @ {self.timestamp}>"

#     @property
#     def is_healthy(self):
#         return self.status == "HEALTHY"

#     @property
#     def memory_available_gb(self):
#         return self.memory_total_gb - self.memory_used_gb

