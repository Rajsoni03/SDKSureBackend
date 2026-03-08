from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer."""

    class Meta:
        model = User
        fields = ["id", "email", "username", "is_staff", "is_superuser", "is_active", "last_login", "date_joined"]
        read_only_fields = ["id", "last_login", "date_joined"]

