from django.urls import path
from . import views

urlpatterns = [
    
    # 게시글 관련
    path('', views.article_list_create),
    path('<int:article_id>/', views.article_detail),
    path('<int:article_id>/like/', views.article_like),

    # 댓글 관련
    path('<int:article_id>/comments/', views.comment_list_create),
    path('comments/<int:comment_id>/', views.comment_detail),


]
