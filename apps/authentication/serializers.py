from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer."""

    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "is_active", "last_login"]
        read_only_fields = ["id", "last_login"]

