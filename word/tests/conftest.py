import pytest
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return do_authenticate


@pytest.fixture
def api__client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_create_authenticate(is_staff=True):
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return do_create_authenticate
