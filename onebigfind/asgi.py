# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import lostandfound.routing  # Import your app's routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onebigfind.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            lostandfound.routing.websocket_urlpatterns  # Your app's WebSocket URL routing
        )
    ),
})
