from django.urls import re_path
from .consumers import Order

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[^/]+)', Order.as_asgi()),
]