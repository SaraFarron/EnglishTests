from django.shortcuts import render, redirect
from .models import *
from .forms import WordForm, CreateUserForm
from .filters import WordFilter
from .decorators import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'user'])
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


@unauthenticated_user
def register_page(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('train:login')

    context = {'form': form}
    return render(request, 'train/register.html', context)


@login_required(login_url='login')
def user_page(request):
    context = {}
    return render(request, 'train/user.html')


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('train:index')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'train/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('train:login')


@login_required(login_url='login')
def word_list(request):
    words = Word.objects.all()
    my_filter = WordFilter(request.GET, queryset=words)
    words_for_filter = my_filter.qs
    context = {'words': words, 'my_filter': words_for_filter}
    return render(request, 'train/word_list.html', context)


@login_required(login_url='login')
def create_translation(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/train/list')
    form = WordForm()
    context = {'form': form}
    return render(request, 'train/create_translation.html', context)


@login_required(login_url='login')
def update_translation(request, pk):
    word = Word.objects.get(id=pk)
    form = WordForm(instance=word)
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('/train/list')
    context = {'form': form}
    return render(request, 'train/create_translation.html', context)


@login_required(login_url='login')
def delete_translation(request, pk):
    word = Word.objects.get(id=pk)
    if request.method == 'POST':
        word.delete()
        return redirect('/train/list')
    context = {'item': word}
    return render(request, 'train/delete_translation.html', context)


@login_required(login_url='login')
def training(request):
    return render(request, 'train/training.html')
