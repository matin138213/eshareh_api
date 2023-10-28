from rest_framework import serializers
from .models import Word, Category


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'title', 'category', 'picture', 'video', 'pronunciation', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug', 'parent', 'picture']
