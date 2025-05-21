from django.urls import path
from . import views

urlpatterns = [
    
    # 초기 데이터 생성
    path('get_deposit_products/',views.get_deposit_products),
    path('get_saving_products/',views.get_saving_products),

    # deposit
    path('deposit/',views.deposit_product_list),
    path('deposit/<int:option_id>/',views.deposit_detail),
    
    # saving
    path('saving/',views.saving_product_list),
    path('saving/<int:option_id>/',views.saving_detail),


    # saving
]
