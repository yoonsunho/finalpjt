from django.urls import path
from . import views

urlpatterns = [
     path('commodity_price/',views.commodity_price),
     ]
