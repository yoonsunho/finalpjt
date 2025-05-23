from django.urls import path
from . import views

urlpatterns = [
    
    # 초기 데이터 생성
    path('get_deposit_products/',views.get_deposit_products),
    path('get_saving_products/',views.get_saving_products),

    # deposit
    path('deposit/',views.deposit_product_list),
    path('deposit/<int:product_id>/',views.deposit_detail),
    path('deposit/<int:product_id>/interest/', views.deposit_interest),
    path('deposit/<int:product_id>/join/', views.deposit_join),
    
    # saving
    path('saving/',views.saving_product_list),
    path('saving/<int:product_id>/',views.saving_detail),
    path('saving/<int:product_id>/interest/',views.saving_interest),
    path('saving/<int:product_id>/join/',views.saving_join),
    
    # 내 목록 조회
    path('my-interests/', views.my_interests),
    path('my-joins/', views.my_joins),


]
