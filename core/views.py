from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.core.cache import cache
from core.seializers import UserPhoneNumber, LoginSerializer
from users.models import CustomUser
import random
from users.tasks import send_sms

# Create your views here.
class UserPhoneNumbers(CreateAPIView):
    serializer_class = UserPhoneNumber

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data['phone_number']
        (username, created) = CustomUser.objects.get_or_create(username=phone_number)
        code=cache.set(phone_number, random.randint(1000, 9999))
        send_sms.delay(to=phone_number,token=code)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class Login(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data['phone_number']
        code = serializer.data['code']
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
