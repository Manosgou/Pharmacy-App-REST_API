from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('hello', views.hello, name="hello"),
    path('login', obtain_auth_token, name="login"),
]