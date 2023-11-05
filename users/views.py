from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action

from word.models import Word
from .models import CustomUser, Interest
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminSuperUser
from .seializers import UserSerializer, InterestSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminSuperUser]

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



class InterestViewSet(ListModelMixin, GenericViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
