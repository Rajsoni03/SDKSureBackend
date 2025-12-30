from django.contrib import admin

from .models import Board, BoardLog, Capability, PCStats, Relay, TestPC


@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    list_display = ("relay_name", "model_type", "status", "ip_address", "port_count", "last_checked_at")
    list_filter = ("status", "model_type")
    search_fields = ("relay_name", "ip_address", "mac_address")


@admin.register(TestPC)
class TestPCAdmin(admin.ModelAdmin):
    list_display = ("hostname", "status", "os_version", "ip_address", "last_heartbeat_at")
    list_filter = ("status", "os_version")
    search_fields = ("hostname", "ip_address", "domain_name")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "platform",
        "status",
        "test_farm",
        "is_alive",
        "is_locked",
        "relay",
        "test_pc",
        "last_heartbeat_at",
    )
    search_fields = ("name", "hardware_serial_number", "project", "board_ip")
    list_filter = ("status", "platform", "test_farm", "is_alive", "is_locked")
    raw_id_fields = ("relay", "test_pc")
    filter_horizontal = ("capabilities",)
    ordering = ("name",)


@admin.register(PCStats)
class PCStatsAdmin(admin.ModelAdmin):
    list_display = ("test_pc", "status", "cpu_percent", "memory_percent", "disk_percent", "timestamp")
    list_filter = ("status",)
    search_fields = ("test_pc__hostname",)
    ordering = ("-timestamp",)


@admin.register(BoardLog)
class BoardLogAdmin(admin.ModelAdmin):
    list_display = ("board", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("board__name", "message")
