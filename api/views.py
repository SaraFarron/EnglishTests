from django.shortcuts import render
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import *
from .serializers import *


class HomeView():
    pass


class ProfileView(ModelViewSet):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.get(id=self.request.user)


class DictionaryView(ListModelMixin, ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class RegistrationView():
    pass


class LoginView():
    pass

# TODO Добавить домашнюю страницу, профиль, список всех вопросов в базе, логин,
#  регистрацию, тестирование
