from rest_framework import serializers

from .models import Label, TestCase, TestType


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name"]


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = ["id", "name", "description"]


class TestCaseSerializer(serializers.ModelSerializer):
    tags = LabelSerializer(many=True, required=False, read_only=True)
    test_type = TestTypeSerializer(read_only=True)

    class Meta:
        model = TestCase
        fields = [
            "id",
            "title",
            "description",
            "test_type",
            "tags",
            "is_active",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
