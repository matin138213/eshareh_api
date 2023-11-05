from io import BytesIO

import pytest
from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from mock import MagicMock
from model_bakery import baker
from rest_framework import status

from djangoProject.utils import create_picture
from word.models import Word


@pytest.fixture
def get_word(api_client):
    def do_get_word():
        return api_client.get('/kalameh/words/')

    return do_get_word


@pytest.fixture
def get_word_id(api_client):
    def do_get_word(id):
        return api_client.get(f'/kalameh/words/{id}/')

    return do_get_word


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
def create_word(api_client):
    def do_create_word(data):
        return api_client.post('/kalameh/words/', data)

    return do_create_word


@pytest.fixture
def add_word_to_interest(api_client):
    def do_create_word_favorite(data, id):
        return api_client.post(f'/kalameh/words/{id}/add_to_word_interest/', data)

    return do_create_word_favorite


@pytest.fixture
def update_word(api_client):
    def do_update_word(data, id):
        return api_client.patch(f'/kalameh/words/{id}/', data)

    return do_update_word


@pytest.fixture
def delete_word(api_client):
    def do_delete_word(id):
        return api_client.delete(f'/kalameh/words/{id}/')

    return do_delete_word


@pytest.mark.django_db
class TestGetWord:
    def test_if_user_is_anonymous_return_401(self, get_word):
        response = get_word()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticad_return_200(self, get_word, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_word()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_anonymous_get_return_401(self, get_word_id):
        word_obj = baker.make(Word)

        response = get_word_id(word_obj.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticaed_get_word_id_return_200(self, get_word_id, api_client, authenticate):
        authenticate(is_staff=False)
        word_obj = baker.make(Word)

        response = get_word_id(word_obj.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticaed_get_word_id_return_404(self, get_word_id, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_word_id(2534562)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateWord:
    def test_if_user_is_anonymous_return_401(self, create_word):
        response = create_word({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, create_word, authenticate):
        authenticate(is_staff=False)

        response = create_word({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, create_word, authenticate):
        authenticate(is_staff=True)

        response = create_word({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, create_word, authenticate):
        authenticate(is_staff=True)
        file = create_picture()

        new_data = post_data.copy()
        new_data['picture'] = file

        response = create_word(data=new_data)
        file.close()

        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestUpdateWord:
    def test_if_user_is_anonymous_patch_return_401(self, update_word):
        word_put = baker.make(Word)

        response = update_word({'title': 'a'}, id=word_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_patch_word_return_400(self, update_word, authenticate):
        authenticate(is_staff=True)
        word_put = baker.make(Word)
        response = update_word({'picture': 124}, id=word_put.id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_patch_return_200(self, update_word, authenticate):
        authenticate(is_staff=True)
        word_put = baker.make(Word)

        response = update_word({'title': 'a'}, id=word_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_not_admin_patch_return_403(self, update_word, authenticate):
        authenticate(is_staff=False)
        word_put = baker.make(Word)

        response = update_word({'title': 'a'}, id=word_put.id)
        print(response.data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_not_admin_patch_return_404(self, update_word, authenticate):
        authenticate(is_staff=True)
        word_put = baker.make(Word)

        response = update_word({'title': 'a'}, id=word_put.id + 100)
        print(response.data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteWord:
    def test_if_user_is_anonymous_delete_return_401(self, delete_word):
        word_delete = baker.make(Word)
        response = delete_word(id=word_delete.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_delete_word_return_403(self, delete_word, authenticate):
        authenticate(is_staff=False)
        word_delete = baker.make(Word)
        response = delete_word(id=word_delete.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_delete_word_return_204(self, delete_word, authenticate):
        authenticate(is_staff=True)
        word_delete = baker.make(Word)
        response = delete_word(id=word_delete.id)
        print(response.data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_admin_delete_return_404(self, delete_word, authenticate):
        authenticate(is_staff=True)
        word_delete = baker.make(Word)

        response = delete_word(id=word_delete.id + 100)
        print(response.data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFavoriteWord:
    def test_if_user_is_anonymous_word_favorite_interest_return_401(self, add_word_to_interest):
        word_delete = baker.make(Word)
        response = add_word_to_interest({'title': 'a'}, id=word_delete.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_favorite_word_return_200(self, add_word_to_interest, authenticate):
        authenticate(is_staff=True)
        word = baker.make(Word)

        file = create_picture()
        new_data = post_data.copy()
        new_data['picture'] = file

        response = add_word_to_interest(data=new_data, id=word.id)
        file.close()

        print(response.data)

        assert response.status_code == status.HTTP_200_OK
