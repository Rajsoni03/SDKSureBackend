import django_filters

from .models import Board, Capability


class BoardFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    project = django_filters.CharFilter(field_name="project", lookup_expr="icontains")
    platform = django_filters.CharFilter(field_name="platform")
    test_farm = django_filters.CharFilter(field_name="test_farm")
    is_locked = django_filters.BooleanFilter(field_name="is_locked")
    is_alive = django_filters.BooleanFilter(field_name="is_alive")
    relay_id = django_filters.UUIDFilter(field_name="relay__id")
    workstation_id = django_filters.UUIDFilter(field_name="workstation__id")
    capabilities = django_filters.ModelMultipleChoiceFilter(
        field_name="capabilities",
        to_field_name="id",
        queryset=Capability.objects.all(),
    )

    class Meta:
        model = Board
        fields = [
            "status",
            "name",
            "project",
            "platform",
            "test_farm",
            "is_locked",
            "is_alive",
            "relay_id",
            "workstation_id",
            "capabilities",
        ]
