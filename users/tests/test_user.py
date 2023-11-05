from io import BytesIO

import pytest
from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from mock import MagicMock
from model_bakery import baker
from rest_framework import status

from djangoProject.utils import create_picture
from users.models import CustomUser


@pytest.fixture
def get_user(api_client):
    def do_get_user():
        return api_client.get('/karbar/users/')

    return do_get_user


@pytest.fixture
def get_me(api_client):
    def do_get_me():
        return api_client.get('/karbar/users/me/')

    return do_get_me


@pytest.fixture
def get_user_id(api_client):
    def do_get_user(id):
        return api_client.get(f'/karbar/users/{id}/')

    return do_get_user


mock_image = MagicMock(spec=File)
mock_image.name = "test.png"
mock_video = MagicMock(spec=File)
mock_video.name = "test.mp4"
post_data = {
    'title': 'a',
    'username': 'a',
    'slug': 'a',
    'pronunciation': 'a',
    'video': mock_video,
    'picture': mock_image,
}


@pytest.fixture
def create_user(api_client):
    def do_create_user(data):
        return api_client.post('/karbar/users/', data)

    return do_create_user


@pytest.fixture
def update_user(api_client):
    def do_update(data, id):
        return api_client.patch(f'/karbar/users/{id}/', data)

    return do_update


@pytest.fixture
def update_me_patch(api_client):
    def do_update_user(data, id):
        return api_client.patch(f'/karbar/users/me/', data)

    return do_update_user


@pytest.fixture
def delete_user(api_client):
    def do_delete(id):
        return api_client.delete(f'/karbar/users/{id}/')

    return do_delete


@pytest.mark.django_db
class TestGetUser:
    def test_if_user_is_anonymous_return_401(self, get_user):
        response = get_user()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_return_200(self, get_user, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_user()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_anonymous_get_user_return_401(self, get_user_id):
        user_obj = baker.make(CustomUser)

        response = get_user_id(user_obj.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_jafar_return_200(self, get_user_id, api_client, authenticate):
        authenticate(is_staff=False)
        user_obj = baker.make(CustomUser)

        response = get_user_id(user_obj.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticaed_get_word_jafar_return_404(self, get_user_id, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_user_id(2534562)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateUser:
    def test_if_user_is_anonymous_return_401(self, create_user):
        response = create_user({'first_name': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, create_user, authenticate):
        authenticate(is_staff=False)

        response = create_user({'first_name': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, create_user, authenticate):
        authenticate(is_staff=True)

        response = create_user({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_return_201(self, create_user, authenticate):
        authenticate(is_staff=True)
        file = create_picture()
        new_data = post_data.copy()
        new_data['picture'] = file

        response = create_user(data=new_data)
        file.close()

        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestUpdateUser:
    def test_if_user_is_anonymous_patch_return_401(self, update_user):
        user_put = baker.make(CustomUser)
        response = update_user({'first_name': 'a'}, id=user_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_patch_return_200(self, update_user, authenticate):
        authenticate(is_staff=True)
        user_put = baker.make(CustomUser)

        response = update_user({'first_name': 'a'}, id=user_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_not_admin_patch_return_403(self, update_user, authenticate):
        authenticate(is_staff=False)
        user_put = baker.make(CustomUser)

        response = update_user({'first_name': 'a'}, id=user_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_user_return_400(self, update_user, authenticate):
        authenticate(is_staff=True)
        user_put = baker.make(CustomUser)

        response = update_user({'picture': 123445}, id=user_put.id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_not_admin_patch_return_404(self, update_user, authenticate):
        authenticate(is_staff=True)
        user_put = baker.make(CustomUser)

        response = update_user({'title': 'a'}, id=user_put.id + 100)
        print(response.data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteUser:
    def test_if_user_is_anonymous_delete_return_401(self, delete_user):
        user_delete = baker.make(CustomUser)
        response = delete_user(id=user_delete.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_delete_user_return_403(self, delete_user, authenticate):
        authenticate(is_staff=False)
        user_delete = baker.make(CustomUser)
        response = delete_user(id=user_delete.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_delete_user_return_204(self, delete_user, authenticate):
        authenticate(is_staff=True)
        user_delete = baker.make(CustomUser)
        response = delete_user(id=user_delete.id)
        print(response.data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_not_admin_delete_user_return_404(self, delete_user, authenticate):
        authenticate(is_staff=True)
        user_delete = baker.make(CustomUser)

        response = delete_user(id=user_delete.id + 100)
        print(response.data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestGetMe:
    def test_if_user_me_anonymous_return_401(self, get_me):
        response = get_me()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_return_200(self, get_me, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_me()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_anonymous_patch_return_401(self, update_me_patch):
        me_put = baker.make(CustomUser)
        response = update_me_patch({'username': 'a'}, id=me_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_admin_patch_return_200(self, update_me_patch, authenticate):
        authenticate(is_staff=True)
        me_put = baker.make(CustomUser)

        response = update_me_patch({'username': 'a'}, id=me_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'a'




