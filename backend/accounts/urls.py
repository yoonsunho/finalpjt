# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check-email/', views.check_email, name='check_email'),
    path('check-nickname/', views.check_nickname, name='check_nickname'),
]
