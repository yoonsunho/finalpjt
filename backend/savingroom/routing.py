# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/savings/(?P<room_id>\d+)/$', consumers.SavingRoomConsumer.as_asgi()),
]
