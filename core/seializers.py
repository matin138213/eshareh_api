from rest_framework import serializers


class UserPhoneNumber(serializers.Serializer):
    phone_number = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code=serializers.IntegerField()
