import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# ✅ 1. 먼저 Django 앱 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backpjt.settings')
django_asgi_app = get_asgi_application()

# ✅ 2. 이후 라우팅 임포트
from savingroom import routing  # 모델 임포트는 초기화 후에!

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(routing.websocket_urlpatterns)
    ),
})
