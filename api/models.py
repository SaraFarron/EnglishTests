from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Word(models.Model):
    russian = models.CharField(max_length=255)
    english = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=100)
    words_for_learning = models.ManyToManyField(Word, blank=True, null=True)
    words_learned = models.ManyToManyField(Word, blank=True, null=True)
