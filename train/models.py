from django.db import models


class Word(models.Model):
    english = models.CharField(max_length=50)
    russian = models.CharField(max_length=50)
    times_learned = models.IntegerField(default=0)
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return self.english


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    words = models.ForeignKey(Word, on_delete=models.CASCADE)
