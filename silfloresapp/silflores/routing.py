from channels.auth import AuthMiddlewareStack #type:ignore
from channels.routing import ProtocolTypeRouter, URLRouter #type:ignore
from django.urls import path, include
from django.contrib import admin
from django.core.asgi import get_asgi_application
import cart.routing
import silflores.urls

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            cart.routing.websocket_urlpatterns
        )
    ),
})