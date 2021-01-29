from django.urls import path
from . import views

app_name = 'train'
urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.word_list, name='list'),
    path('training', views.training, name='training'),
    # path('<int:word_id>/answer', views.answer, name='answer'),
]
