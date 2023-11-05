import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient, force_authenticate

from users.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=baker.make(CustomUser, is_staff=is_staff))

    return do_authenticate
