from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.HomeView, name='home'),
    path('list/', views.DictionaryView, name='dictionary'),

    path('register', views.RegistrationView, name='register'),
    path('login', views.LoginView, name='login'),
    # path('logout', views.logout_user, name='logout'),
    path('user/<int:pk>', views.ProfileView, name='profile'),
]

