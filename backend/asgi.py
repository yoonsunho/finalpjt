import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# ✅ Set Django settings first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backpjt.settings')

# ✅ Initialize Django BEFORE importing anything that uses models
django_asgi_app = get_asgi_application()

# ✅ Now it's safe to import modules that use Django models
from savingroom.routing import websocket_urlpatterns
from savingroom.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    )
})