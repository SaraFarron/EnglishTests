from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    english = models.CharField(max_length=50)
    russian = models.CharField(max_length=50)
    times_learned = models.IntegerField(default=0)
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return self.english


class Pupil(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
