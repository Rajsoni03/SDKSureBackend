from django.contrib import admin
from .models import Capability, Relay, Workstation, Board

# Register your models here.

@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    list_display = ("relay_name", "model_type", "status", "ip_address", "port_count", "last_checked_at")
    list_filter = ("status", "model_type")
    search_fields = ("relay_name", "ip_address")


@admin.register(Workstation)
class WorkstationAdmin(admin.ModelAdmin):
    list_display = ("hostname", "status", "os_version", "ip_address", "cpu_utilization", "ram_utilization", "disk_utilization", "docker_container_count", "last_heartbeat_at")
    list_filter = ("status", "os_version")
    search_fields = ("hostname", "ip_address", "domain_name")
    list_editable = ("status",)
    ordering = ("hostname",)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "platform",
        "status",
        "test_farm",
        "is_alive",
        "relay",
        "workstation",
        "last_heartbeat_at",
    )
    search_fields = ("name", "hardware_serial_number", "project", "board_ip")
    list_filter = ("status", "platform", "test_farm", "is_alive")
    raw_id_fields = ("relay", "workstation")
    filter_horizontal = ("capabilities",)
    list_editable = ("status", "is_alive")
    ordering = ("name",)


# @admin.register(PCStats)
# class PCStatsAdmin(admin.ModelAdmin):
#     list_display = ("workstation", "status", "cpu_percent", "memory_percent", "disk_percent", "timestamp")
#     list_filter = ("status",)
#     search_fields = ("workstation__hostname",)
#     ordering = ("-timestamp",)
