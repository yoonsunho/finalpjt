from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_email>/',views.recommend_view, name='recommend'),
]