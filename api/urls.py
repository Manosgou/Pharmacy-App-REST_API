from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('hello', views.hello, name="hello"),
    path('login', obtain_auth_token, name="login"),
    path('logout', views.logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user/update/<int:id>', views.user_update, name="user_update"),
]