from django.urls import re_path

from .consumers import TestRunConsumer

websocket_urlpatterns = [
    re_path(r"ws/test-runs/(?P<testrun_id>[^/]+)/$", TestRunConsumer.as_asgi()),
]

