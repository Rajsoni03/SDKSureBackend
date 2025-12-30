from rest_framework import serializers

from .models import Board, BoardLog, Capability, PCStats, Relay, TestPC


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
            "mac_address",
            "port_count",
            "created_at",
            "updated_at",
            "last_checked_at",
            "is_healthy",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_checked_at", "is_healthy"]


class TestPCSerializer(serializers.ModelSerializer):
    is_online = serializers.ReadOnlyField()
    is_available_for_testing = serializers.ReadOnlyField()

    class Meta:
        model = TestPC
        fields = [
            "id",
            "hostname",
            "ip_address",
            "domain_name",
            "status",
            "os_version",
            "disk_mountpoint",
            "location",
            "comment",
            "created_at",
            "updated_at",
            "last_heartbeat_at",
            "is_online",
            "is_available_for_testing",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_heartbeat_at", "is_online", "is_available_for_testing"]


class PCStatsSerializer(serializers.ModelSerializer):
    is_healthy = serializers.ReadOnlyField()
    memory_available_gb = serializers.ReadOnlyField()

    class Meta:
        model = PCStats
        fields = [
            "id",
            "test_pc",
            "status",
            "memory_total_gb",
            "memory_used_gb",
            "memory_free_gb",
            "memory_percent",
            "disk_total_gb",
            "disk_used_gb",
            "disk_free_gb",
            "disk_percent",
            "cpu_percent",
            "network_io_read_mb",
            "network_io_write_mb",
            "process_count",
            "thread_count",
            "timestamp",
            "is_healthy",
            "memory_available_gb",
        ]
        read_only_fields = ["id", "timestamp", "is_healthy", "memory_available_gb"]


class BoardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardLog
        fields = ["id", "board", "message", "level", "created_at"]
        read_only_fields = ["id", "created_at"]


class BoardSerializer(serializers.ModelSerializer):
    capabilities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Capability.objects.all(),
        required=False,
    )
    capability_details = CapabilitySerializer(source="capabilities", many=True, read_only=True)
    relay = RelaySerializer(read_only=True)
    relay_id = serializers.PrimaryKeyRelatedField(
        source="relay",
        queryset=Relay.objects.all(),
        allow_null=True,
        required=False,
    )
    test_pc = TestPCSerializer(read_only=True)
    test_pc_id = serializers.PrimaryKeyRelatedField(
        source="test_pc",
        queryset=TestPC.objects.all(),
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
            "execution_engine",
            "test_farm",
            "sdk_version",
            "status",
            "is_alive",
            "is_locked",
            "board_ip",
            "relay_id",
            "relay_number",
            "relay",
            "test_pc_id",
            "test_pc",
            "location",
            "last_sdk_update_at",
            "description",
            "notes",
            "created_at",
            "updated_at",
            "last_used_at",
            "last_heartbeat_at",
            "capabilities",
            "capability_details",
            "can_execute_test",
            "is_healthy",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "last_used_at",
            "last_heartbeat_at",
            "capability_details",
            "relay",
            "test_pc",
            "can_execute_test",
            "is_healthy",
        ]
