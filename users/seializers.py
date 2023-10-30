from rest_framework import serializers
from .models import CustomUser, Interest


class UserSerializer(serializers.ModelSerializer):
    # is_vip = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'is_vip', 'picture']
        read_only_fields = ['is_vip']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'word']
