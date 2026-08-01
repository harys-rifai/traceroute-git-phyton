import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import network_globe.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_globe.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(network_globe.routing.websocket_urlpatterns)
    ),
})
