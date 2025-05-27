from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

@sync_to_async
def get_user_by_token(token_key):
    """Get user by token key"""
    if not token_key:
        logger.warning("No token provided")
        return AnonymousUser()

    try:
        # ✅ 여기서 import! 앱 초기화 후에 실행되므로 OK
        from rest_framework.authtoken.models import Token
        token = Token.objects.select_related('user').get(key=token_key)
        logger.info(f"Token validated for user: {token.user.nickname}")
        return token.user
    except Exception as e:
        logger.warning(f"Token error: {e}")
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "websocket":
            return await super().__call__(scope, receive, send)

        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get("token", [None])[0]

        user = await get_user_by_token(token_key)
        scope["user"] = user

        if not user.is_anonymous:
            logger.info(f"WebSocket auth: User {user.nickname} authenticated")
        else:
            logger.warning("WebSocket auth: Anonymous user")

        return await super().__call__(scope, receive, send)
