"""Hardware board and infrastructure models."""
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Capability(models.Model):
    """Represents a capability that a board can support."""

    CAPABILITY_CHOICES = [
        ("CMD", _("Command Execution")),
        ("CAMERA", _("Camera Testing")),
        ("DISPLAY", _("Display Output")),
        ("SOUND", _("Sound/Audio")),
        ("FILE", _("File System")),
        ("SENSOR", _("Sensor Reading")),
        ("GPIO", _("GPIO Control")),
        ("ADC", _("Analog-to-Digital")),
        ("NETWORK", _("Network Connectivity")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier")
    name = models.CharField(max_length=50, choices=CAPABILITY_CHOICES, unique=True, help_text="Capability name")
    description = models.TextField(blank=True, help_text="Detailed description of this capability")
    is_active = models.BooleanField(default=True, help_text="Whether this capability can be used")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = _("Capabilities")
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.get_name_display()}"

    def __repr__(self):
        return f"<Capability: {self.name}>"


class Relay(models.Model):
    """Represents a power or network relay used to control boards."""

    STATUS_CHOICES = [
        ("ACTIVE", _("Active")),
        ("INACTIVE", _("Inactive")),
        ("MAINTENANCE", _("Maintenance")),
        ("FAULT", _("Fault")),
    ]

    MODEL_TYPE_CHOICES = [
        ("POWER_EXTENSION", _("Power Extension")),
        ("ETH_008_A", _("Ethernet 008 Type A")),
        ("ETH_008_B", _("Ethernet 008 Type B")),
        ("ETH_016", _("Ethernet 016")),
        ("CUSTOM", _("Custom")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    relay_name = models.CharField(max_length=100, unique=True, help_text="Unique name for this relay")
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES, help_text="Type of relay")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="INACTIVE", help_text="Relay status")
    location = models.CharField(max_length=200, blank=True, help_text="Physical location (e.g., Rack A, Shelf 2)")
    ip_address = models.GenericIPAddressField(unique=True, help_text="IP address of the relay")
    mac_address = models.CharField(
        max_length=17,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                message="Enter a valid MAC address",
            )
        ],
        help_text="MAC address in format XX:XX:XX:XX:XX:XX",
    )
    port_count = models.PositiveIntegerField(
        default=8,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Number of ports on this relay",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_checked_at = models.DateTimeField(null=True, blank=True, help_text="Last health check timestamp")

    class Meta:
        ordering = ("relay_name",)
        verbose_name_plural = _("Relays")
        indexes = [
            models.Index(fields=["ip_address"]),
            models.Index(fields=["mac_address"]),
            models.Index(fields=["status"]),
            models.Index(fields=["relay_name"]),
        ]

    def __str__(self):
        return f"{self.relay_name} ({self.ip_address})"

    def __repr__(self):
        return f"<Relay: {self.relay_name}>"

    @property
    def is_healthy(self):
        return self.status == "ACTIVE"


class TestPC(models.Model):
    """Represents a test execution PC/machine."""

    STATUS_CHOICES = [
        ("ONLINE", _("Online")),
        ("OFFLINE", _("Offline")),
        ("MAINTENANCE", _("Maintenance")),
        ("INITIALIZING", _("Initializing")),
    ]

    OS_VERSION_CHOICES = [
        ("ubuntu_18_04", "Ubuntu 18.04 LTS"),
        ("ubuntu_20_04", "Ubuntu 20.04 LTS"),
        ("ubuntu_22_04", "Ubuntu 22.04 LTS"),
        ("ubuntu_24_04", "Ubuntu 24.04 LTS"),
        ("centos_7", "CentOS 7"),
        ("centos_8", "CentOS 8"),
        ("centos_9", "CentOS 9"),
        ("windows_10", "Windows 10"),
        ("windows_11", "Windows 11"),
        ("macos_ventura", "macOS Ventura"),
        ("macos_sonoma", "macOS Sonoma"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hostname = models.CharField(max_length=255, unique=True, help_text="Hostname of the PC")
    ip_address = models.GenericIPAddressField(unique=True, help_text="IP address of the PC")
    domain_name = models.CharField(max_length=255, blank=True, help_text="FQDN of the PC")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OFFLINE", help_text="PC status")
    os_version = models.CharField(max_length=50, choices=OS_VERSION_CHOICES, help_text="Operating system version")
    disk_mountpoint = models.CharField(max_length=255, default="/", help_text="Primary disk mount point")
    location = models.CharField(max_length=255, blank=True, help_text="Physical location in lab/datacenter/rack")
    comment = models.TextField(blank=True, help_text="Additional notes about this PC")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_heartbeat_at = models.DateTimeField(null=True, blank=True, help_text="Last heartbeat received from this PC")

    class Meta:
        ordering = ("hostname",)
        verbose_name = _("Test PC")
        verbose_name_plural = _("Test PCs")
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
        return f"<TestPC: {self.hostname}>"

    @property
    def is_online(self):
        return self.status == "ONLINE"

    @property
    def is_available_for_testing(self):
        return self.status in ["ONLINE", "INITIALIZING"]


class PCStats(models.Model):
    """Performance statistics for a TestPC."""

    STATUS_CHOICES = [
        ("HEALTHY", _("Healthy")),
        ("WARNING", _("Warning")),
        ("CRITICAL", _("Critical")),
        ("UNKNOWN", _("Unknown")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_pc = models.ForeignKey(
        TestPC,
        on_delete=models.CASCADE,
        related_name="performance_stats",
        help_text="Reference to the TestPC",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="UNKNOWN", help_text="Overall health")
    memory_total_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Total memory in GB")
    memory_used_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Used memory in GB")
    memory_free_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Free memory in GB")
    memory_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Memory usage percentage",
    )
    disk_total_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Total disk space in GB")
    disk_used_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Used disk space in GB")
    disk_free_gb = models.FloatField(validators=[MinValueValidator(0)], help_text="Free disk space in GB")
    disk_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Disk usage percentage",
    )
    cpu_percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="CPU usage percentage"
    )
    network_io_read_mb = models.FloatField(default=0, help_text="Network read in MB")
    network_io_write_mb = models.FloatField(default=0, help_text="Network write in MB")
    process_count = models.PositiveIntegerField(help_text="Number of active test processes")
    thread_count = models.PositiveIntegerField(help_text="Number of active test threads")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True, help_text="When this stat was recorded")

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = _("PC Stats")
        verbose_name_plural = _("PC Stats")
        indexes = [
            models.Index(fields=["test_pc", "-timestamp"]),
            models.Index(fields=["status", "-timestamp"]),
            models.Index(fields=["-timestamp"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(memory_percent__gte=0) & models.Q(memory_percent__lte=100),
                name="memory_percent_range",
            ),
        ]

    def __str__(self):
        return f"{self.test_pc.hostname} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def __repr__(self):
        return f"<PCStats: {self.test_pc.hostname} @ {self.timestamp}>"

    @property
    def is_healthy(self):
        return self.status == "HEALTHY"

    @property
    def memory_available_gb(self):
        return self.memory_total_gb - self.memory_used_gb


class Board(models.Model):
    """Hardware board (EVM) model."""

    PLATFORM_CHOICES = [
        ("j721s2", "TI J721S2"),
        ("j721e", "TI J721E"),
        ("j722s", "TI J722S"),
        ("j742s2", "TI J742S2"),
        ("j784s4", "TI J784S4"),
        ("j7200", "TI J7200"),
        ("am62x", "TI AM62x"),
        ("am62px", "TI AM62Px"),
    ]

    STATUS_CHOICES = [
        ("IDLE", _("Idle")),
        ("BUSY", _("Busy")),
        ("UPDATING_SDK", _("Updating SDK")),
        ("OFFLINE", _("Offline")),
        ("DEACTIVATED", _("Deactivated")),
        ("ERROR", _("Error")),
    ]

    TEST_FARM_CHOICES = [
        ("HLOS", _("HLOS (Linux/QNX)")),
        ("RTOS", _("RTOS (Real-Time OS)")),
        ("BAREMETAL", _("Bare-metal")),
        ("STAGING", _("Staging")),
        ("INTEGRATION", _("Integration")),
    ]

    DEVICE_TYPE_CHOICES = [
        ("EVM", _("Evaluation Module")),
        ("SOCKET_BOARD", _("Socket Board")),
        ("BREAKOUT_BOARD", _("Breakout Board")),
        ("CUSTOM", _("Custom")),
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
        help_text="Type of device",
    )
    pg_version = models.CharField(max_length=100, blank=True, help_text="Processor SDK or software version")
    execution_engine = models.CharField(max_length=100, blank=True, help_text="Test execution engine")
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
    test_pc = models.ForeignKey(
        TestPC,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="boards",
        help_text="TestPC that controls this board",
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
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["hardware_serial_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_alive"]),
            models.Index(fields=["test_farm"]),
            models.Index(fields=["project"]),
            models.Index(fields=["platform"]),
            models.Index(fields=["test_pc"]),
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
            and self.test_pc
            and self.test_pc.is_available_for_testing
        )

    @property
    def is_healthy(self):
        return self.is_alive and self.status != "ERROR"

    def get_available_capabilities(self):
        return self.capabilities.filter(is_active=True)

    def mark_seen(self):
        self.last_heartbeat_at = timezone.now()
        self.save(update_fields=["last_heartbeat_at"])


class BoardLog(models.Model):
    """Log entries for board connectivity and execution events."""

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="logs")
    message = models.TextField()
    level = models.CharField(
        max_length=10, choices=[("INFO", "INFO"), ("WARN", "WARN"), ("ERROR", "ERROR")], default="INFO"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.board.name}: {self.level}"
