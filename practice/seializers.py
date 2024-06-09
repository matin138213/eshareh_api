from rest_framework import serializers

from word.models import Word
from word.serializers import SimpleCategorySerializer


class WordSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()

    class Meta:
        model = Word
        fields = ['id', 'title', 'category', 'picture', 'video', 'pronunciation', 'slug']


class VipWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'title', 'category', 'picture', 'pronunciation', 'slug']


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'video']
class VipWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'title', 'category', 'picture', 'pronunciation', 'slug']

