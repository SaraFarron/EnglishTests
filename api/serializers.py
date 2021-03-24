from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ("russian", "english")
