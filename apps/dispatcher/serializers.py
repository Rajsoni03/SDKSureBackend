from rest_framework import serializers

from apps.dispatcher.models import TestRequest


class DispatchRequestSerializer(serializers.Serializer):
    platform = serializers.CharField()
    required_capabilities = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    priority = serializers.IntegerField(required=False, default=0)
    timeout = serializers.IntegerField(required=False, default=600)

    def validate(self, attrs):
        caps = {cap.strip() for cap in attrs.get("required_capabilities", []) if cap.strip()}
        attrs["required_capabilities"] = sorted(caps)
        return attrs


class TestRequestSerializer(serializers.ModelSerializer):
    capability_list = serializers.SerializerMethodField()

    class Meta:
        model = TestRequest
        fields = [
            "id",
            "platform",
            "priority",
            "required_capabilities",
            "capability_list",
            "status",
            "timeout",
            "executed_on_board",
            "executed_on_pc",
            "created_at",
            "started_at",
            "completed_at",
        ]
        read_only_fields = fields

    def get_capability_list(self, obj):
        if not obj.required_capabilities:
            return []
        return [cap for cap in obj.required_capabilities.split(",") if cap]


class CompleteRequestSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    success = serializers.BooleanField(required=False, default=True)
