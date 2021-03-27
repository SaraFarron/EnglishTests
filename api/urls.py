from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'api'
router = DefaultRouter()

router.register('home', views.HomeViewSet, basename='home')
router.register('dictionary', views.DictionaryViewSet, basename='dictionary')
router.register('train', views.TrainingViewSet, basename='train')

router.register('register', views.RegistrationViewSet, basename='register')
router.register('login', views.LoginViewSet, basename='login')
router.register('profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    url(r'^', include(router.urls)),
]
