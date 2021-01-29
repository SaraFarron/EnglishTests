from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseRedirect
# from django.urls import reverse
from .models import *


def index(request):
    words = Word.objects.all()
    number_of_words = len(words)
    number_of_learned_words = 0
    number_of_words_in_progress = 0
    for word in words:
        if word.is_learned:
            number_of_learned_words += 1
        elif word.times_learned != 0:
            number_of_words_in_progress += 1
    return render(request, 'index.html', {
        'number_of_words': number_of_words,
        'number_of_learned_words': number_of_learned_words,
        'number_of_words_in_progress': number_of_words_in_progress
    })


def word_list(request):
    return render(request, 'train/word_list.html')


def training(request):
    return render(request, 'train/training.html')