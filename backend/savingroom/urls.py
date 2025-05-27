# from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path


urlpatterns = [
    path('', views.room_list),      # 방 목록/생성:
    path('<int:room_id>/', views.room_detail),  # 방 상세
    path('<int:room_id>/join/', views.join_room),   # 방 참가
    path('<int:room_id>/deposit/', views.make_deposit), # 입금
    path('my-rooms/created/',views.my_created_rooms),   # 내가 만든 방
    path('my-rooms/joined/',views.my_joined_rooms),  # 내가 참가한 방'
    path('my-rooms/all/',views.my_all_rooms),  # 내가 참가한 방'
    
]
