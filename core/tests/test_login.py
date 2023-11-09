import random

import pytest
from model_bakery import baker
from rest_framework import status
from django.core.cache import cache
from users.models import CustomUser


@pytest.fixture
def create_user_phone_number(api_client):
    def do_create_user_login(data):
        return api_client.post('/login/usernumber/', data)

    return do_create_user_login


@pytest.fixture
def create_user_login(api_client):
    def do_create_user_login(data):
        return api_client.post('/login/login/', data)

    return do_create_user_login


@pytest.mark.django_db
class TestCreateUserNumber:
    def test_if_data_is_invalid_return_400(self, create_user_phone_number, authenticate):
        authenticate(is_staff=True)

        response = create_user_phone_number({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_return_201(self, create_user_phone_number, authenticate):
        authenticate(is_staff=True)
        response = create_user_phone_number({'phone_number': '09050912664'})
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestCreateLogin:
    def test_if_data_is_invalid_return_400(self, create_user_login, authenticate):
        authenticate(is_staff=True)

        response = create_user_login({})
        print(response.data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_return_201(self, create_user_login,create_user_phone_number, authenticate):
        authenticate(is_staff=True)
        user = baker.make(CustomUser)
        response_1= create_user_phone_number({'phone_number':'09191538285'})
        code=cache.get('09191538285')
        response = create_user_login({'phone_number': '09191538285', 'code': code})
        print(response_1.data)

        assert response.status_code == status.HTTP_201_CREATED
