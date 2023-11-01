from itertools import chain
from operator import add

from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from users.models import Interest
from users.seializers import InterestSerializer
from .models import Word, Category
from .permissions import IsAdminSuperUser
from .serializers import WordSerializer, CategorySerializer, SimpleWordSerializer,UploadSerializer
# Create your views here.
class WordViewSet(ModelViewSet):
    queryset = Word.objects.select_related('category').all()
    serializer_class = WordSerializer
    permission_classes = [IsAdminSuperUser]
    filterset_fields = ['category']
    search_fields = ['title']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WordSerializer
        return SimpleWordSerializer

    @action(detail=True, methods=['POST'])
    def add_to_word_interest(self, request, pk):
        word = get_object_or_404(Word, pk=pk)
        (favorite, created) = Interest.objects.get_or_create(user=self.request.user)
        if word in favorite.word.all():
            favorite.word.remove(word)
            return Response('add to bookmark word no')
        else:
            favorite.word.add(word)
            return Response('add to bookmark word yes')


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminSuperUser]
    filterset_fields = ['parent']
