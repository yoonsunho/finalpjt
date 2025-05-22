from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('finlife/',include('finlife.urls')),
    path('accounts/', include('accounts.urls')),  # ← 이 줄 추가!
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
]
