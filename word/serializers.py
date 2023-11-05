
from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField

from .models import Word, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'picture']


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class WordSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()

    class Meta:
        model = Word
        fields = ['id', 'title', 'category', 'picture', 'video', 'pronunciation', 'slug']


class SimpleWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'title', 'category', 'picture', 'video', 'pronunciation', 'slug']


