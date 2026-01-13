import logging

import pytest
from rest_framework.test import APIClient

logging.disable(logging.CRITICAL)


@pytest.fixture
def api_client():
    return APIClient()

