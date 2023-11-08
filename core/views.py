from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from core.seializers import UserPhoneNumber, LoginSerializer
from users.models import CustomUser
import random
from users.tasks import send_sms
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class UserPhoneNumbers(CreateAPIView):
    serializer_class = UserPhoneNumber
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data['phone_number']
        (username, created) = CustomUser.objects.get_or_create(username=phone_number)
        code = random.randint(1000, 9999)
        print(code)
        cache.set(phone_number,code , timeout=60 * 2)
        # send_sms.delay(to=phone_number, token=1234)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class Login(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.data['phone_number']
        code = serializer.data['code']
        user = CustomUser.objects.get(username=phone_number)

        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        headers = self.get_success_headers(serializer.data)

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
