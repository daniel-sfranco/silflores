from channels.auth import AuthMiddlewareStack #type:ignore
from channels.routing import ProtocolTypeRouter, URLRouter #type:ignore
from django.urls import path, include #type:ignore
from django.contrib import admin #type:ignore
from django.core.asgi import get_asgi_application #type:ignore
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