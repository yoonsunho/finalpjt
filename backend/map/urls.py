from django.urls import path
from . import views

urlpatterns = [
    path('map_data/', views.map_data),                # 전체 데이터 (시/도, 시/군/구, 은행)
    path('countries/', views.countries),             # 특정 시/도에 대한 시/군/구
    path('search/', views.search_banks),          # 은행 지점 검색 (카카오 API)
]