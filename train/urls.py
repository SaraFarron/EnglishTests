from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'train'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.WordList.as_view, name='list'),
    path('training/', views.training, name='training'),

    path('list/add/', views.CreateTranslation.as_view, name='create_translation'),
    path('list/update/<str:pk>/', views.UpdateTranslation.as_view, name='update_translation'),
    path('list/delete/<str:pk>/', views.DeleteTranslation.as_view, name='delete_translation'),

    path('register', views.register_page, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),

    path('user/', views.user_page, name='user_page'),

    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
