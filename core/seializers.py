import re

from rest_framework import serializers
from django.core.cache import cache
from users.models import CustomUser


class UserPhoneNumber(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate(self, data):
        if cache.get(data['phone_number']):
            raise serializers.ValidationError("لطفا 2 دقیقه صبر کنید")
        pattern = r'^09[0-9]{9}$'#re to argoman
        if not re.match(pattern, data['phone_number']):
            raise serializers.ValidationError("شماره موبایل نامعتبر هست")

        return data


# pattern = r'^09[0-9]{9}$'
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.IntegerField(max_value=9999)

    def validate(self, data):
        if not CustomUser.objects.filter(username=data['phone_number']).exists():
            raise serializers.ValidationError("شماره تلفن شما اشتباه است!")
        if cache.get(data['phone_number']) != data['code']:
            raise serializers.ValidationError("کد اشتباه است")

        return data
