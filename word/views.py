import random

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Word, Category
from .paginations import DefaultPagination
from .permissions import IsAdminSuperUser
from .serializers import WordSerializer, CategorySerializer, SimpleCategorySerializer, SimpleWordSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


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


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminSuperUser]
    filterset_fields = ['parent']


