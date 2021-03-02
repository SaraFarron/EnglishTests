from django.shortcuts import render, redirect

from .models import *
from .forms import WordForm, CreateUserForm
from .filters import WordFilter
from .decorators import *

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly


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
            Pupil.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('train:login')

    context = {'form': form}
    return render(request, 'train/register.html', context)


@login_required(login_url='login')
def user_page(request):

    words = request.user.pupil.word_set.all()
    total_words = words.count()
    learned = words.filter(is_learned=True).count()
    not_learned = words.filter(is_learned=False).count()

    context = {'words': words, 'total_words': total_words,
               'learned': learned, 'not_learned': not_learned
               }
    return render(request, 'train/user.html', context)


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


# @csrf_exempt
# def snippet_list(request):
#     """List all code snippets, or create a new snippet."""
#
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def snippet_detail(request, pk):
#     """Retrieve, update or delete a code snippet."""
#
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)


# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     """List all code snippets, or create a new snippet."""
#
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     """Retrieve, update or delete a code snippet."""
#
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetList(APIView):
    """List all snippets, or create a new snippet."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(APIView):
    """Retrieve, update or delete a snippet instance."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



