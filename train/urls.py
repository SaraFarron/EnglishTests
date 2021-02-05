from django.urls import path
from . import views

app_name = 'train'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.word_list, name='list'),
    path('training/', views.training, name='training'),

    path('list/add/', views.create_translation, name='create_translation'),
    path('list/update/<str:pk>/', views.update_translation, name='update_translation'),
    path('list/delete/<str:pk>/', views.delete_translation, name='delete_translation'),

    path('register', views.register_page, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
]
