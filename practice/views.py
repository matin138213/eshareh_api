import random

from django.shortcuts import render
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# from practice.filters import SentenceFilter
from practice.seializers import VipWordSerializer, SentenceSerializer
from word.models import Word
from word.serializers import WordSerializer


# Create your views here.
class ExamViewSet(ListModelMixin, GenericViewSet):
    serializer_class = WordSerializer

    def get_queryset(self):
        return random.choices(Word.objects.all(), k=4)

    def get_serializer_class(self):
        if not self.request.user.is_vip:
            return VipWordSerializer
        return WordSerializer


class SentenceViewSet(ListModelMixin, GenericViewSet):
    serializer_class = SentenceSerializer

    def get_queryset(self):
        try:
            id = self.request.GET.get('id')
            id = id.split(',')  # There was an ID, come to separate and filter based on the ID of the word
            return Word.objects.filter(pk__in=id)
        except Exception:
            return []
