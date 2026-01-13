from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    """Serializer for outgoing websocket events."""

    type = serializers.CharField()
    payload = serializers.JSONField()

