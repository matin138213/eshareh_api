from django_filters.rest_framework import FilterSet
from .models import Word, Category


class WordFilter(FilterSet):
    class Meta:
        model = Word
        fields = {
            'category': ['exact'],
        }


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'parent': ['exact'],
        }
