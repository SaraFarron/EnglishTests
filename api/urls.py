from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.HomeView.as_view, name='home'),
    path('list/', views.DictionaryView.as_view, name='dictionary'),

    path('register', views.RegistrationView.as_view, name='register'),
    path('login', views.LoginView.as_view, name='login'),
    # path('logout', views.logout_user, name='logout'),
    path('user/<int:pk>', views.ProfileView.as_view, name='profile'),
]

