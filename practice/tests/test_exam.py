from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
import pytest
from word.models import Word
from model_bakery import baker
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth.models import User
from mock import MagicMock
from django.core.files import File


@pytest.fixture
def get_word_exam(api_client):
    def do_get_word_exam():
        return api_client.get('/practice/exams/')

    return do_get_word_exam


@pytest.mark.django_db
class TestGetWord:
    def test_if_user_is_anonymous_return_401(self, get_word_exam):
        response = get_word_exam()
        print(response.data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_return_200(self, get_word_exam, api_client, authenticate):
        authenticate(is_staff=False)
        word= baker.make(Word, _quantity=4)

        response = get_word_exam()

        assert response.status_code == status.HTTP_200_OK

