import json
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
def get_word_sen(api_client):
    def do_get_word_sen(ids_list):
        ids = ','.join(str(id) for id in ids_list)
        print(ids)
        return api_client.get(f'/practice/sentences/?id={ids}')

    return do_get_word_sen


@pytest.mark.django_db
class TestGetWord:
    def test_if_user_is_anonymous_return_401(self, get_word_sen):
        word = baker.make(Word)
        word2 = baker.make(Word)

        response = get_word_sen([word.id, word2.id])

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticaed_return_200(self, get_word_sen, api_client, authenticate):
        authenticate(is_staff=False)
        word = baker.make(Word)
        word2 = baker.make(Word)

        response = get_word_sen([word.id, word2.id])
        print(json.dumps(response.data))
        result=response.data['results']
        ids=[matin['id'] for matin in result]

        assert response.status_code == status.HTTP_200_OK
        assert word2.id in ids and word.id in ids


