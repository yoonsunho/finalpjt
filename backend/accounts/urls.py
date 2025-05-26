# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check-email/', views.check_email, name='check_email'),
    path('check-nickname/', views.check_nickname, name='check_nickname'),
    path('myprofile/', views.my_profile_view, name='my_profile'),
    path('myprofile/change-password/', views.change_password, name='change_password'),
    path('google/',views.google_login),
    path('complete-social-signup/',views.complete_social_signup)
]
