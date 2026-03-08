from rest_framework import serializers

from .models import Board, Capability, Relay, Workstation


class CapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capability
        fields = ["id", "name", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class RelaySerializer(serializers.ModelSerializer):
    is_healthy = serializers.ReadOnlyField()

    class Meta:
        model = Relay
        fields = [
            "id",
            "relay_name",
            "model_type",
            "status",
            "location",
            "ip_address",
            "username",
            "password",
            "port_count",
            "notes",
            "created_at",
            "updated_at",
            "last_checked_at",
            "is_healthy",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_checked_at", "is_healthy"]


class WorkstationSerializer(serializers.ModelSerializer):
    is_online = serializers.ReadOnlyField()
    is_available_for_testing = serializers.ReadOnlyField()

    class Meta:
        model = Workstation
        fields = [
            "id",
            "hostname",
            "ip_address",
            "domain_name",
            "auth_token",
            "workarea",
            "status",
            "os_version",
            "disk_mountpoint",
            "location",
            "cpu_utilization",
            "ram_utilization",
            "disk_utilization",
            "docker_container_count",
            "notes",
            "created_at",
            "updated_at",
            "last_heartbeat_at",
            "is_online",
            "is_available_for_testing",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_heartbeat_at", "is_online", "is_available_for_testing"]


class BoardSerializer(serializers.ModelSerializer):
    capabilities = CapabilitySerializer(many=True, read_only=True)
    capability_ids = serializers.PrimaryKeyRelatedField(
        source="capabilities",
        many=True,
        queryset=Capability.objects.all(),
        required=False,
        write_only=True,
    )
    relay = RelaySerializer(read_only=True)
    relay_id = serializers.PrimaryKeyRelatedField(
        source="relay",
        queryset=Relay.objects.all(),
        allow_null=True,
        required=False,
    )
    workstation = WorkstationSerializer(read_only=True)
    workstation_id = serializers.PrimaryKeyRelatedField(
        source="workstation",
        queryset=Workstation.objects.all(),
        allow_null=True,
        required=False,
    )
    can_execute_test = serializers.ReadOnlyField()
    is_healthy = serializers.ReadOnlyField()

    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "hardware_serial_number",
            "project",
            "platform",
            "device_type",
            "pg_version",
            "test_farm",
            "sdk_version",
            "status",
            "is_alive",
            "is_locked",
            "board_ip",
            "capabilities",
            "capability_ids",
            "relay_id",
            "relay_number",
            "relay",
            "workstation_id",
            "workstation",
            "location",
            "last_sdk_update_at",
            "description",
            "notes",
            "created_at",
            "updated_at",
            "last_used_at",
            "last_heartbeat_at",
            "can_execute_test",
            "is_healthy",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "last_used_at",
            "last_heartbeat_at",
            "relay",
            "workstation",
            "can_execute_test",
            "is_healthy",
        ]

    def create(self, validated_data):
        capabilities = validated_data.pop("capabilities", [])
        board = super().create(validated_data)
        if capabilities:
            board.capabilities.set(capabilities)
        return board

    def update(self, instance, validated_data):
        capabilities = validated_data.pop("capabilities", None)
        board = super().update(instance, validated_data)
        if capabilities is not None:
            board.capabilities.set(capabilities)
        return board


# class PCStatsSerializer(serializers.ModelSerializer):
#     is_healthy = serializers.ReadOnlyField()
#     memory_available_gb = serializers.ReadOnlyField()

#     class Meta:
#         model = PCStats
#         fields = [
#             "id",
#             "workstation",
#             "status",
#             "memory_total_gb",
#             "memory_used_gb",
#             "memory_free_gb",
#             "memory_percent",
#             "disk_total_gb",
#             "disk_used_gb",
#             "disk_free_gb",
#             "disk_percent",
#             "cpu_percent",
#             "network_io_read_mb",
#             "network_io_write_mb",
#             "process_count",
#             "thread_count",
#             "timestamp",
#             "is_healthy",
#             "memory_available_gb",
#         ]
#         read_only_fields = ["id", "timestamp", "is_healthy", "memory_available_gb"]
