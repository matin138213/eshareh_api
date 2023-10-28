from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import WordFilter, CategoryFilter
from .models import Word, Category
from .paginations import DefaultPagination
from .permissions import IsAdminSuperUser
from .serializers import WordSerializer, CategorySerializer


# Create your views here.
class WordViewSet(ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAdminSuperUser]
    filterset_class = WordFilter
    pagination_class = DefaultPagination
    search_fields = ['title']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAdminSuperUser]
    filterset_class = CategoryFilter
