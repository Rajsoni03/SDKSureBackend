from rest_framework import serializers

from apps.test_cases.models import Label, TestCase
from apps.test_cases.serializers import LabelSerializer
from .models import TestResult, TestRun, TestScenario


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ["id", "status", "message", "created_at"]
        read_only_fields = ["id", "created_at"]


class TestCaseSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ["id", "title"]


class TestScenarioSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSummarySerializer(many=True, read_only=True)
    test_case_ids = serializers.PrimaryKeyRelatedField(
        source="test_cases",
        many=True,
        queryset=TestCase.objects.all(),
        required=False,
        write_only=True,
    )
    labels = LabelSerializer(many=True, read_only=True)
    label_ids = serializers.PrimaryKeyRelatedField(
        source="labels",
        many=True,
        queryset=Label.objects.all(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = TestScenario
        fields = [
            "id",
            "name",
            "description",
            "test_cases",
            "test_case_ids",
            "labels",
            "label_ids",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "test_cases", "labels", "created_by", "updated_by", "created_at", "updated_at"]

    def create(self, validated_data):
        test_cases = validated_data.pop("test_cases", [])
        labels = validated_data.pop("labels", [])
        scenario = super().create(validated_data)
        if test_cases:
            scenario.test_cases.set(test_cases)
        if labels:
            scenario.labels.set(labels)
        return scenario

    def update(self, instance, validated_data):
        test_cases = validated_data.pop("test_cases", None)
        labels = validated_data.pop("labels", None)
        scenario = super().update(instance, validated_data)
        if test_cases is not None:
            scenario.test_cases.set(test_cases)
        if labels is not None:
            scenario.labels.set(labels)
        return scenario


class TestRunSerializer(serializers.ModelSerializer):
    results = TestResultSerializer(many=True, read_only=True)
    scenarios = TestScenarioSerializer(many=True, read_only=True)
    scenario_ids = serializers.PrimaryKeyRelatedField(
        source="scenarios",
        many=True,
        queryset=TestScenario.objects.all(),
        required=False,
        write_only=True,
    )
    labels = LabelSerializer(many=True, read_only=True)
    label_ids = serializers.PrimaryKeyRelatedField(
        source="labels",
        many=True,
        queryset=Label.objects.all(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = TestRun
        fields = [
            "id",
            "name",
            "description",
            "scenarios",
            "scenario_ids",
            "labels",
            "label_ids",
            "results",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "scenarios", "labels", "results", "created_by", "updated_by", "created_at", "updated_at"]

    def create(self, validated_data):
        scenarios = validated_data.pop("scenarios", [])
        labels = validated_data.pop("labels", [])
        run = super().create(validated_data)
        if scenarios:
            run.scenarios.set(scenarios)
        if labels:
            run.labels.set(labels)
        return run

    def update(self, instance, validated_data):
        scenarios = validated_data.pop("scenarios", None)
        labels = validated_data.pop("labels", None)
        run = super().update(instance, validated_data)
        if scenarios is not None:
            run.scenarios.set(scenarios)
        if labels is not None:
            run.labels.set(labels)
        return run
