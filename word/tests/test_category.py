from io import BytesIO

import pytest
from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from mock import MagicMock
from model_bakery import baker
from rest_framework import status

from djangoProject.utils import create_picture
from word.models import Category


@pytest.fixture
def get_category(api_client):
    def do_get_category(id=None):
        if id:
            return api_client.get(f'/kalameh/category/{id}/')
        return api_client.get('/kalameh/category/')

    return do_get_category


@pytest.fixture
def get_category_id(api_client):
    def do_category_word(id):
        return api_client.get(f'/kalameh/category/{id}/')

    return do_category_word


mock_image = MagicMock(spec=File)
mock_image.name = "test.png"
mock_video = MagicMock(spec=File)
mock_video.name = "test.mp4"
post_data = {
    'title': 'a',
    'slug': 'a',
    'pronunciation': 'a',
    'video': mock_video,
    'picture': mock_image,
}


@pytest.fixture
def create_category(api_client):
    def do_create_category(data):
        return api_client.post('/kalameh/category/', data)

    return do_create_category


@pytest.fixture
def update_category(api_client):
    def do_update(data, id):
        return api_client.patch(f'/kalameh/category/{id}/', data)

    return do_update


@pytest.fixture
def delete_category(api_client):
    def do_delete(id):
        return api_client.delete(f'/kalameh/category/{id}/')

    return do_delete


@pytest.mark.django_db
class TestGetCategory:
    def test_if_anonymous_get_category_return_401(self, get_category):
        response = get_category()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_get_category_return_200(self, get_category, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_category()

        assert response.status_code == status.HTTP_200_OK

    def test_if_anonymous_retrieve_category_return_401(self, get_category_id):
        category_obj = baker.make(Category)

        response = get_category_id(category_obj.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_retrive_category_return_200(self, get_category_id, api_client, authenticate):
        authenticate(is_staff=False)
        category_obj = baker.make(Category)

        response = get_category_id(category_obj.id)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticaed_get_word_return_404(self, get_category_id, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_category_id(2534562)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateCategory:
    def test_if_user_is_anonymous_return_401(self, create_category):
        response = create_category({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, create_category, authenticate):
        authenticate(is_staff=False)

        response = create_category({})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, create_category, authenticate):
        authenticate(is_staff=True)

        response = create_category({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, create_category, authenticate):
        authenticate(is_staff=True)
        file = create_picture()
        new_data = post_data.copy()
        new_data['picture'] = file

        response = create_category(data=new_data)
        file.close()
        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUpdateCategory:
    def test_if_user_is_anonymous_patch_return_401(self, update_category):
        category_put = baker.make(Category)
        response = update_category({}, id=category_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_patch_return_200(self, update_category, authenticate):
        authenticate(is_staff=True)
        category_put = baker.make(Category)

        response = update_category({'title': 'a'}, id=category_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_not_admin_patch_return_403(self, update_category, authenticate):
        authenticate(is_staff=False)
        category_put = baker.make(Category)

        response = update_category({'title': 'a'}, id=category_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_category_return_400(self, update_category, authenticate):
        authenticate(is_staff=True)
        category_put = baker.make(Category)

        response = update_category({'picture':124},id=category_put.id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_not_admin_patch_return_404(self, update_category, authenticate):
        authenticate(is_staff=True)
        category_put = baker.make(Category)

        response = update_category({'title': 'a'}, id=category_put.id + 100)
        print(response.data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCategory:
    def test_if_user_is_anonymous_delete_category_return_401(self, delete_category):
        category_delete = baker.make(Category)

        response = delete_category(id=category_delete.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_word_return_403(self, delete_category, authenticate):
        authenticate(is_staff=False)
        category_delete = baker.make(Category)

        response = delete_category(id=category_delete.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_delete_word_return_204(self, delete_category, authenticate):
        authenticate(is_staff=True)
        category_delete = baker.make(Category)

        response = delete_category(id=category_delete.id)
        print(response.data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_not_admin_delete_return_404(self, delete_category, authenticate):
        authenticate(is_staff=True)
        category_delete = baker.make(Category)

        response = delete_category(id=category_delete.id + 100)
        print(response.data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
