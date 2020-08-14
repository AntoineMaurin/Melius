from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.user_login),
    path('register', views.register),
    path('logout', views.user_logout),
]
