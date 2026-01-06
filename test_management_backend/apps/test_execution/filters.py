import django_filters

from .models import TestRun


class TestRunFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    scenario = django_filters.NumberFilter(field_name="scenarios__id")
    label = django_filters.NumberFilter(field_name="labels__id")

    class Meta:
        model = TestRun
        fields = ["name", "scenario", "label"]
