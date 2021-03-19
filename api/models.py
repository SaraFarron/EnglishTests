from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=100)
    # добавить поле со словами
