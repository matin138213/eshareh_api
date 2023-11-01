from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
import pytest
from word.models import Word
from model_bakery import baker
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth.models import User



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


@pytest.fixture
def create_word(api_client):
    def do_create_word(data):
        return api_client.post('/kalameh/words/', data)

    return do_create_word


@pytest.mark.django_db
class TestGetWord:
    def test_if_user_is_anonymous_return_401(self, get_word):
        # client = APIClient()

        response = get_word()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_return_200(self, get_word, api_client, authenticate):
        authenticate(is_staff=False)

        response = get_word()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_anonymous_get_return_401(self, get_word_id):
        word_obj = baker.make(Word)

        response = get_word_id(word_obj.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_jafar_return_200(self, get_word_id, api_client, authenticate):
        authenticate(is_staff=False)
        word_obj = baker.make(Word)
        response = get_word_id(word_obj.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticaed_get_word_jafar_return_404(self, get_word_id, api_client, authenticate):
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

    import pytest
    from django.core.files.uploadedfile import SimpleUploadedFile
    from django.urls import reverse

    def test_if_data_is_valid_return_201(self, create_word, authenticate):
        authenticate(is_staff=True)

        response = create_word({'title': 'a', 'pronunciation': 'a', 'slug': 'a', 'video':'BASE_DIR/media/film',
                                'picture': 'BASE_DIR/media/images'})
        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


