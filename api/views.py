from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import viewsets

from .models import *
from .serializers import *


class HomeViewSet(ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.get(id=self.request.user)


class DictionaryViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    serializer_class = WordSerializer
    queryset = Word.objects.all()


class RegistrationViewSet(ModelViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TrainingViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id).words_for_learning  # ошибка входа

# TODO Добавить регистрацию, тестирование
